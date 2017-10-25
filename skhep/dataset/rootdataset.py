# Licensed under a 3-clause BSD style license, see LICENSE.
"""
**********************
Module for ROOTDataset
**********************

The ``ROOTDataset`` class is the implementation of the ``Dataset`` abstract base class
for the [ROOT]_ package.

Note: usage of course requires that ROOT is installed.

**References**

.. [ROOT] https://root.cern.ch/.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from os.path import isfile
import glob
from types import MethodType

from ..utils.py23 import *
from ..utils.decorators import inheritdoc
from ..utils.dependencies import softimport
from ..utils.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting

from .defs import *

ROOT = softimport("ROOT")
root_numpy = softimport("root_numpy")


# -----------------------------------------------------------------------------
# ROOTDataset
# -----------------------------------------------------------------------------
class ROOTDataset(FromFiles, ToFiles, NewNumpy, Dataset):
    def __init__(self, data, provenance=None):
        """Default constructor for ROOTDataset.

        Parameters
        ----------
        data: a TTree or TChain instance.
        provenance: history of the data before being wrapped as a ROOTDataset.
        """
        self._data = data
        if isinstance(data, ROOT.TChain) and (provenance is None):
            provenance = FileOrigin([f.GetTitle() for f in data.GetListOfFiles()])
        elif isinstance(data, ROOT.TTree) and (provenance is None):
            provenance = ObjectOrigin(data.GetName())
        self._provenance = provenance

    @property
    @inheritdoc(Dataset)
    def datashape(self):
        raise NotImplementedError  # TODO!

    @property
    @inheritdoc(Dataset)
    def immutable(self): return False

    @property
    @inheritdoc(Dataset)
    # ROOT datasets exist in a form that survives the Python session (feature that is different from Numpy)
    def persistent(self):
        return True

    @staticmethod
    def from_file(files, **options):
        """
        Load a dataset from a file or collection of files.

        files: string file name, glob pattern or iterable of string file names.
        options:
            treename: str, name of the TTree object in the collection of files.
                      Optional only if all input files contain a single TTree, with the same name.
        """
        if isinstance(files, str):
            files = glob.glob(files)
        treename = options.get("treename")
        from root_numpy import list_trees #TODO: avoid the dependency
        if treename is None:
            notOK = []
            treenames = set()
            for fname in files: #TODO: check the case when there are no trees in a file!
                trees = list_trees(fname)
                if len(trees) != 1: notOK.append(fname)
                treenames.add(trees[0])
            if notOK:
                raise ValueError("Multiple trees found in file(s) {0}!\nPlease specify a tree name.".format(','.join(notOK)))
            if len(treenames) > 1:
                raise ValueError("Different tree names found!\nPlease specify the desired tree name.")
            treename = treenames.pop()
            del notOK, treenames
        else:
            notOK = []
            for fname in files: #TODO: check the case when there are no trees in a file!
                trees = list_trees(fname)
                if trees[0] != treename:  notOK.append(fname)
            if notOK:
                raise ValueError("Specified tree name '{0}'' not found in file(s) {1}!\nPlease check your inputs.".format(treename,','.join(notOK)))

        chain = ROOT.TChain(treename)
        for name in list(files):
            n = chain.Add(name)

        return ROOTDataset(chain, FileOrigin([f.GetTitle() for f in chain.GetListOfFiles()]))

    @inheritdoc(ToFiles, gap="\n")
    def to_file(self, base, **options):
        """
        options:
            mode: ROOT's mode in which the TFile is to be opened. Default='update'.
        """
        mode = 'update' if options.get("mode") is None else options.get("mode")
        outfile = ROOT.TFile(base, mode)
        if not outfile:
            raise IOError("Cannot open file {0}! TTree not saved.".format(base))
        if not outfile.IsWritable():
            raise IOError("File {0} is not writable!".format(base))
        # If a tree with that name exists, we want to update it
        treename = self.data.GetName()
        tree = outfile.Get(treename)
        tree = self.data
        tree.Write(treename, ROOT.TObject.kOverwrite) # Save only the new version of the tree
        del tree
        outfile.Close()
        del outfile

    @inheritdoc(NewNumpy, gap="\n")
    def newNumpy(self, **options):
        """
        options: see options of root_numpy.tree2array.
        """
        ar = root_numpy.tree2array(self.data, options)
        from .numpydataset import NumpyDataset
        return NumpyDataset(ar, self._provenance + (Formatting("NumpyDataset"),))

    def __getitem__(self, name):
        raise NotImplementedError  # TODO!


# -----------------------------------------------------------------------------
# Add ROOT methods to ROOTDataset in bulk.
# -----------------------------------------------------------------------------
def addROOTMethod(method):
    raise NotImplementedError  # TODO!


try:
    pass
    # ... (see numpydataset.py)
except ImportError:
    pass

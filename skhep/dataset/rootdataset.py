# Licensed under a 3-clause BSD style license, see LICENSE.
"""
***********************
Module for NumpyDataset
***********************
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from types import MethodType

from .defs import *
from ..util.py23 import *
from ..util.decorators import inheritdoc
from ..util.dependencies import softimport
from ..util.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting

ROOT = softimport("ROOT")
root_numpy = softimport("root_numpy")

#-----------------------------------------------------------------------------
# ROOTDataset
#-----------------------------------------------------------------------------

class ROOTDataset(FromFiles, ToFiles, NewNumpy, Dataset):
    def __init__(self, fileName, provenance=None):
        """Default constructor for ROOTDataset.

        fileName: string name or glob pattern of ROOT files on disk
        provenance: history of the data before being wrapped as a ROOTDataset
        """

        self._data = None

        if provenance is None:
            provenance = FileOrigin(fileName)
        self._provenance = provenance

    @inheritdoc(Dataset)
    def schema(self):
        raise NotImplementedError    # TODO!

    @inheritdoc(Dataset)
    def immutable(self): return False

    @inheritdoc(Dataset)
    def persistent(self): return True   # a ROOT feature that is different from Numpy
    
    @staticmethod
    def fromFiles(files, **options):
        return ROOTDataset(files)

    @inheritdoc(ToFiles, gap="\n")
    def toFiles(self, base, **options):
        raise NotImplementedError    # TODO!

    @inheritdoc(NewROOT)
    def newNumpy(self, **options):
        """options: none"""
        raise NotImplementedError    # TODO!

        out = root_numpy.root2array()

        from .rootdataset import ROOTDataset
        return NumpyDataset(out, self.provenance + (Formatting("NumpyDataset"),))

    def __getitem__(self, name):
        raise NotImplementedError    # TODO!

#-----------------------------------------------------------------------------
# Add ROOT methods to ROOTDataset in bulk.
#-----------------------------------------------------------------------------

def addROOTMethod(method):
        raise NotImplementedError    # TODO!

try:
    pass
    # ... (see numpydataset.py)

except ImportError:
    pass

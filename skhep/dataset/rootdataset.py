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

from types import MethodType

from .defs import *
from ..utils.py23 import *
from ..utils.decorators import inheritdoc
from ..utils.dependencies import softimport
from ..utils.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting

ROOT = softimport("ROOT")
root_numpy = softimport("root_numpy")


# -----------------------------------------------------------------------------
# ROOTDataset
# -----------------------------------------------------------------------------
class ROOTDataset(FromFiles, ToFiles, NewNumpy, Dataset):
    def __init__(self, file_name, provenance=None):
        """Default constructor for ROOTDataset.

        file_name: string name or glob pattern of ROOT files on disk
        provenance: history of the data before being wrapped as a ROOTDataset
        """

        self.__data = None

        if provenance is None:
            provenance = FileOrigin(file_name)
        self.__provenance = provenance

    @inheritdoc(Dataset)
    def datashape(self):
        raise NotImplementedError  # TODO!

    @inheritdoc(Dataset)
    def immutable(self): return False

    @inheritdoc(Dataset)
    # a ROOT feature that is different from Numpy
    def persistent(self): return True

    @staticmethod
    def fromFiles(files, **options):
        return ROOTDataset(files)

    @inheritdoc(ToFiles, gap="\n")
    def toFiles(self, base, **options):
        raise NotImplementedError  # TODO!

    @inheritdoc(NewROOT)
    def newNumpy(self, **options):
        """options: none"""
        raise NotImplementedError  # TODO!

        out = root_numpy.root2array()

        from .rootdataset import ROOTDataset
        return NumpyDataset(out, self.__provenance + (Formatting("NumpyDataset"),))

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

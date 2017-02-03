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

from .defs import *
from ..util.py23 import *
from ..util.decorators import inheritdoc
from ..util.dependencies import softimport
from ..util.provenance import FileOrigin, ObjectOrigin, Transformation

numpy = softimport("numpy")

#-----------------------------------------------------------------------------
# NumpyDataset
#-----------------------------------------------------------------------------

class NumpyDataset(FromFiles, ToFiles, NewNumpy, NewROOT, Dataset):
    @staticmethod
    def isrecarray(data):
        return isinstance(data, numpy.recarray)

    @staticmethod
    def isdictof1d(data):
        return isinstance(data, dict) and len(data) > 0 and all(isinstance(column, numpy.ndarray) and len(column.shape) == 1 for column in data.values()) and all(column.shape == head(data.values()).shape for column in data.values())

    def __init__(self, data, provenance=None):
        """Default constructor for NumpyDataset.

        data: a dictionary of equal-length, one-dimensional Numpy arrays or, equivalently, a Numpy record array
        provenance: history of the data before being wrapped as a NumpyDataset
        """

        assert self.isrecarray(data) or self.isdictof1d(data)
        self._data = data

        if provenance is None:
            provenance = ObjectOrigin(repr(data))
        self._provenance = provenance

    @inheritdoc(Dataset)
    def schema(self):
        raise NotImplementedError    # TODO!

    @inheritdoc(Dataset)
    def immutable(self): return False

    @inheritdoc(Dataset)
    def persistent(self): return False
    
    @staticmethod
    def fromFiles(files, **options):
        """Load a Dataset from a file or collection of files.

        Recognizes zipped Numpy (.npz) format.

        files: a string file name (glob pattern), iterable of string file names, or an iterable of files open for reading (binary).
        options:
            columns: a set of columns to select from the files
        """

        requestedColumns = options.get("columns")

        columns = None
        data = None

        for x in NumpyDataset._openFileNames(files):
            npzfile = numpy.load(x)

            if requestedColumns is not None:
                assert set(requestedColumns).issubset(set(npzfile.keys()))

            if columns is None:
                if requestedColumns is None:
                    columns = set(npzfile.keys())
                else:
                    columns = set(requestedColumns)

            newdata = dict((column, npzfile[column]) for column in columns)
            assert NumpyDataset.isdictof1d(newdata)

            if data is None:
                data = newdata
            else:
                data = dict((column, numpy.hstack(data[column], newdata[column])) for column in columns)

        return NumpyDataset(data, FileOrigin(files))

    @inheritdoc(ToFiles, gap="\n")
    def toFiles(self, **options):
        """options: none"""
        raise NotImplementedError

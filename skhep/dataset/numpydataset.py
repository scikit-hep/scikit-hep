# Licensed under a 3-clause BSD style license, see LICENSE.
"""
***********************
Module for NumpyDataset
***********************

The ``NumpyDataset`` class is the implementation of the ``Dataset`` abstract base class
for the [NumPy]_ package.

Note: usage of course requires that NumPy is installed.

**References**

.. [NumPy] http://www.numpy.org/.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from types import MethodType

from .defs import *
from ..utils.py23 import *
from ..utils.decorators import inheritdoc
from ..utils.dependencies import softimport
from ..utils.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting

numpy = softimport("numpy")
root_numpy = softimport("root_numpy")

#-----------------------------------------------------------------------------
# NumpyDataset
#-----------------------------------------------------------------------------

class NumpyDataset(FromFiles, ToFiles, NewROOT, Dataset):
    @staticmethod
    def isrecarray(data):
        return isinstance(data, numpy.recarray) or (isinstance(data, numpy.ndarray) and isinstance(data.dtype.names, tuple) and len(data.dtype.names) > 0)

    @staticmethod
    def isdictof1d(data):
        return isinstance(data, dict) and len(data) > 0 and all(isinstance(column, numpy.ndarray) and len(column.shape) == 1 for column in data.values()) and all(column.shape == head(data.values()).shape for column in data.values())

    def __init__(self, data, provenance=None, **options):
        """Default constructor for NumpyDataset.

        data: a dictionary of equal-length, one-dimensional Numpy arrays or, equivalently, a Numpy record array
        provenance: history of the data before being wrapped as a NumpyDataset
        options: none
        """

        assert self.isrecarray(data) or self.isdictof1d(data)
        self.__data = data

        if provenance is None:
            provenance = ObjectOrigin(repr(data))
        self.__provenance = provenance

    @inheritdoc(Dataset)
    def datashape(self):
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

            # always read column-wise: collection of 1d arrays in a zip file (.npz)
            # (not too different from what ROOT is, actually)
            newdata = dict((column, npzfile[column]) for column in columns)
            assert NumpyDataset.isdictof1d(newdata)

            if data is None:
                data = newdata
            else:
                data = dict((column, numpy.hstack(data[column], newdata[column])) for column in columns)

        if data is None:
            raise IOError("Empty set of files: {0}".format(files))

        return NumpyDataset(data, FileOrigin(files))

    @inheritdoc(ToFiles, gap="\n")
    def toFiles(self, base, **options):
        """options: none"""

        # always write column-wise: collection of 1d arrays in a zip file (.npz)
        # (not too different from what ROOT is, actually)
        if self.isrecarray(self.data):
            data = dict((name, self.data[name]) for name in self.data.dtype.names)
        else:
            data = self.data

        numpy.savez(NumpyDataset._openSingleFile(base), **data)

    @inheritdoc(NewROOT)
    def newROOT(self, fileName, **options):
        """
        fileName: string name of ROOT file
        options: none    # but consider file update vs recreate, etc.
        """

        if self.isrecarray(self.data):
            data = self.data
        elif self.isdictof1d(self.data):
            data = numpy.empty(head(self.__data.values()).shape, dtype=[(name, self.data[name].dtype) for name in self.data])
            for name in self.data:
                data[name] = self.data[name]
        else:
            assert False, "data must be a Numpy record array or a Python dictionary of 1d Numpy arrays."

        root_numpy.array2root(data, fileName, mode="recreate")

        from .rootdataset import ROOTDataset
        return ROOTDataset(fileName, self.__provenance + (Formatting("ROOTDataset", fileName),))

    def __getitem__(self, name):
        return self.data[name]

#-----------------------------------------------------------------------------
# Add Numpy methods to NumpyDataset in bulk.
#-----------------------------------------------------------------------------

def addNumpyMethod(method):
    def fn(self, name, *args, **kwds):
        return method.__call__(self.data, *args, **kwds)

    fn.__name__ = method.__name__
    fn.__doc__ = method.__doc__
    setattr(NumpyDataset, method.__name__, MethodType(fn, None, NumpyDataset))

try:
    addNumpyMethod(numpy.ndarray.__add__)
    addNumpyMethod(numpy.ndarray.__mul__)
    addNumpyMethod(numpy.ndarray.sum)
    addNumpyMethod(numpy.ndarray.mean)
    # ...

except ImportError:
    pass

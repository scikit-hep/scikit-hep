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

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

import sys
from types import MethodType

from ..utils.py23 import *
from ..utils.decorators import inheritdoc
from ..utils.dependencies import softimport
from ..utils.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting

from .defs import *

numpy = softimport("numpy")
root_numpy = softimport("root_numpy")


# -----------------------------------------------------------------------------
# NumpyDataset
# -----------------------------------------------------------------------------
class NumpyDataset(FromFiles, ToFiles, NewROOT, Dataset):
    def __init__(self, data, provenance=None, **options):
        """Default constructor for NumpyDataset.

        Parameters
        ----------
        data: a dictionary of equal-length, one-dimensional Numpy arrays or, equivalently, a Numpy record array.
        provenance: history of the data before being wrapped as a NumpyDataset.
        options: none.
        """
        assert self.isrecarray(data) or self.isdictof1d(data)
        self._data = data

        if provenance is None:
            provenance = ObjectOrigin(repr(data))
        self._provenance = provenance

    @staticmethod
    def isrecarray(data):
        is_valid_recarray = isinstance(data, numpy.recarray)
        is_valid_array = (isinstance(data, numpy.ndarray) and
                          isinstance(data.dtype.names, tuple) and
                          len(data.dtype.names) > 0)
        return is_valid_recarray or is_valid_array

    @staticmethod
    def isdictof1d(data):
        is_dict = isinstance(data, dict)
        is_non_empty = len(data) > 0
        has_only_valid_columns = all(isinstance(column, numpy.ndarray) and len(column.shape) == 1
                                     for column in data.values())
        columns_have_valid_shape = all(column.shape == head(data.values()).shape for column in data.values())
        return is_dict and is_non_empty and has_only_valid_columns and columns_have_valid_shape

    @property
    @inheritdoc(Dataset)
    def datashape(self):
        raise NotImplementedError  # TODO!

    @property
    @inheritdoc(Dataset)
    def immutable(self):
        return False

    @property
    @inheritdoc(Dataset)
    def persistent(self):
        return False

    @staticmethod
    def from_file(files, **options):
        """
        Load a dataset from a file or collection of files.

        Recognizes zipped Numpy (.npz) format.

        files: a string file name (glob pattern), iterable of string file names, or an iterable of files open for reading (binary).
        options:
            columns: a set of columns to select from the files.
        """
        requested_columns = options.get("columns")

        columns = None
        data = None

        for x in NumpyDataset._openFileNames(files):
            npzfile = numpy.load(x)

            if requested_columns is not None:
                assert set(requested_columns).issubset(set(npzfile.keys()))

            if columns is None:
                if requested_columns is None:
                    columns = set(npzfile.keys())
                else:
                    columns = set(requested_columns)

            # always read column-wise: collection of 1d arrays in a zip file (.npz)
            # (not too different from what ROOT is, actually)
            newdata = dict((column, npzfile[column]) for column in columns)
            assert NumpyDataset.isdictof1d(newdata)

            if data is None:
                data = newdata
            else:
                data = dict((column, numpy.hstack(
                    data[column], newdata[column])) for column in columns)

        if data is None:
            raise IOError("Empty set of files: {0}".format(files))

        return NumpyDataset(data, FileOrigin(files))

    @inheritdoc(ToFiles, gap="\n")
    def to_file(self, base, **options):
        """options: none"""
        # always write column-wise: collection of 1d arrays in a zip file (.npz)
        # (not too different from what ROOT is, actually)
        if self.isrecarray(self.data):
            data = dict((name, self.data[name])
                        for name in self.data.dtype.names)
        else:
            data = self.data
        numpy.savez(NumpyDataset._openSingleFile(base), **data)

    @inheritdoc(NewROOT, gap='')
    def to_tree(self, treename, **options):
        """
        Parameters
        ----------
        treename: str
            Name of ROOT TTree to be created.
        options: none

        Returns
        -------
        ROOTDataset holding new ROOT TTree.
        """

        if self.isrecarray(self.data):
            data = self.data
        elif self.isdictof1d(self.data):
            data = numpy.empty(head(self._data.values()).shape,
                               dtype=[(name, self.data[name].dtype) for name in self.data])
            for name in self.data:
                data[name] = self.data[name]
        else:
            assert False, "data must be a Numpy record array or a Python dictionary of 1d Numpy arrays."

        tree = root_numpy.array2tree(self.data, treeename)
        from .rootdataset import ROOTDataset
        return ROOTDataset(tree, self._provenance+(Formatting('ROOTDataset', treename),))

    def __getitem__(self, name):
        return self.data[name]


# -----------------------------------------------------------------------------
# Add Numpy methods to NumpyDataset in bulk.
# -----------------------------------------------------------------------------
def addNumpyMethod(method):
    def fn(self, name, *args, **kwds):
        return method.__call__(self.data, *args, **kwds)

    fn.__name__ = method.__name__
    fn.__doc__ = method.__doc__
    if sys.version_info.major==2:  # ugly but works! TODO: find nicer way
        setattr(NumpyDataset, method.__name__, MethodType(fn, None, NumpyDataset))
    else:
        setattr(NumpyDataset, method.__name__, MethodType(fn, NumpyDataset))

try:
    addNumpyMethod(numpy.ndarray.__add__)
    addNumpyMethod(numpy.ndarray.__mul__)
    addNumpyMethod(numpy.ndarray.sum)
    addNumpyMethod(numpy.ndarray.mean)
except ImportError:
    pass

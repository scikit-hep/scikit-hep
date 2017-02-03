# Licensed under a 3-clause BSD style license, see LICENSE.
"""
******************************
Module for Dataset definitions
******************************
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

import glob

from ..util.py23 import *

#-----------------------------------------------------------------------------
# Generic Dataset
#-----------------------------------------------------------------------------

class Dataset(object):
    def __init__(self):
        raise TypeError("Dataset is an abstract base class; instantiate one of its subclasses insteadone of its subclasses instead.")

    @property
    def data(self):
        """The data underlying this Dataset.

        Use this to pass the data to an external library (without provenance).
        """
        return self._data

    @property
    def provenance(self):
        """The series of transformations that produced this dataset as a tuple."""
        return self._provenance

    @property
    def schema(self):
        """Every Dataset has a Schema, which describes its data types and possibly units in a unified way."""
        raise NotImplementedError

    @property
    def immutable(self):
        """If True, this Dataset cannot be modified in place, only transformed.

        Opposite of mutable.
        """
        raise NotImplementedError

    @property
    def mutable(self):
        """If True, this Dataset can be modified in place.

        Opposite of immutable.
        """
        return not self.immutable

    @property
    def persistent(self):
        """If True, this Dataset exists in a form that survives the Python session, such as a file or database.

        If mutable, changes in this Dataset are reflected in that persistent form.

        Opposite of transient.
        """
        raise NotImplementedError

    @property
    def transient(self):
        """If True, this Dataset only exists in the Python session; changes will be lost if it is not saved.

        If mutable, changes in this Dataset do not propagate back to its source, if any.

        Opposite of persistent.
        """
        return not self.persistent

#-----------------------------------------------------------------------------
# Mixins declaring functionality
#-----------------------------------------------------------------------------

# By adding methods with mixins, we enforce more uniformity than duck typing.
# Only supported methods appear when the user tab-completes.
# A generic dataset can be tested for functionality with isinstance.

class FromPersistent(object): pass
class ToPersistent(object): pass
class ConvertibleInPlace(object): pass
class ConvertibleCopy(object): pass

class FromFiles(FromPersistent):
    @staticmethod
    def _openFileNames(files):
        if isinstance(files, string_types):
            files = glob.glob(files)
        for x in files:
            if isinstance(x, string_types):
                x = open(x, "rb")
            assert isinstance(x, file) and "r" in x.mode
            yield x

    @staticmethod
    def fromFiles(files, **options):
        """Load a Dataset from a file or collection of files.

        files: a string file name (glob pattern), iterable of string file names, or an iterable of files open for reading (binary).
        """
        # NOTE: can't @inheritdoc because this is a @staticmethod
        raise NotImplementedError

class ToFiles(FromPersistent):
    def toFiles(self, base, **options):
        """Save this Dataset to a file or collection of files."""
        raise NotImplementedError
        
class AsNumpy(ConvertibleInPlace):
    def asNumpy(self, **options):
        """View this Dataset as a NumpyDataset, sharing their underlying data.

        A change in the NumpyDataset modifies the original.
        """
        raise NotImplementedError

class NewNumpy(ConvertibleCopy):
    def newNumpy(self, **options):
        """Copy this Dataset into a new NumpyDataset, without sharing any underlying data.

        A change in the NumpyDataset leaves the original untouched.
        """
        raise NotImplementedError

class AsROOT(ConvertibleInPlace):
    def asROOT(self, **options):
        """View this Dataset as a ROOTDataset, sharing their underlying data.

        A change in the ROOTDataset modifies the original.
        """
        raise NotImplementedError

class NewROOT(ConvertibleCopy):
    def newROOT(self, **options):
        """Copy this Dataset into a new ROOTDataset, without sharing any underlying data.

        A change in the ROOTDataset leaves the original untouched.
        """
        raise NotImplementedError

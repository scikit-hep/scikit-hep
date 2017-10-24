# Licensed under a 3-clause BSD style license, see LICENSE.
"""
**************************************
Module for Dataset-related definitions
**************************************

The module contains the definition of the ``Dataset`` abstract base class
and a series of mixin classes.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

import glob

from ..utils.py23 import *


# -----------------------------------------------------------------------------
# Generic Dataset
# -----------------------------------------------------------------------------
class Dataset(object):
    """
    Abstract base class for all dataset classes.
    """

    def __init__(self):
        raise TypeError(
            "Dataset is an abstract base class; instantiate one of its subclasses insteadone of its subclasses instead.")

    @property
    def data(self):
        """The actual data underlying this dataset.

        Use this to pass the data to an external library (without provenance).
        """
        return self.__data

    @property
    def provenance(self):
        """The series of transformations that produced this dataset as a tuple."""
        return self.__provenance

    @property
    def datashape(self):
        """Every dataset has a datashape, which describes its data types in a unified way."""
        # There is a standard for this:
        #     http://libndtypes.readthedocs.io/en/latest/datashape.html
        # We should use it!
        raise NotImplementedError

    @property
    def immutable(self):
        """If True, this dataset cannot be modified in place, only transformed.

        Opposite of mutable.
        """
        raise NotImplementedError

    @property
    def mutable(self):
        """If True, this dataset can be modified in place.

        Opposite of immutable.
        """
        return not self.immutable

    @property
    def persistent(self):
        """If True, this dataset exists in a form that survives the Python session, such as a file or database.

        If mutable, changes in this dataset are reflected in that persistent form.

        Opposite of transient.
        """
        raise NotImplementedError

    @property
    def transient(self):
        """If True, this dataset only exists in the Python session; changes will be lost if it is not saved.

        If mutable, changes in this dataset do not propagate back to its source, if any.

        Opposite of persistent.
        """
        return not self.persistent


# -----------------------------------------------------------------------------
# Mixins declaring functionality
# -----------------------------------------------------------------------------

# By adding methods with mixins, we enforce more uniformity than duck typing.
# Only supported methods appear when the user tab-completes.
# A generic dataset can be tested for functionality with isinstance.
class FromPersistent(object):
    pass


class ToPersistent(object):
    pass


class ConvertibleInPlace(object):
    pass


class ConvertibleCopy(object):
    pass


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
    def from_file(files, **options):
        """Load a dataset from a file or collection of files.

        files: a string file name (glob pattern), iterable of string file names, or an iterable of files open for reading (binary).
        options: optional, of course!
            May contain relevant parameters to pass to the concrete implementation.
        """
        # NOTE: can't @inheritdoc because this is a @staticmethod
        raise NotImplementedError


class ToFiles(ToPersistent):
    @staticmethod
    def _openRolloverFiles(base, rollover_pattern=None):
        """Generic method to generate an infinite series of files with _1, _2, etc. in their names."""
        if rollover_pattern is None:
            # TODO: Rewrite this using os.path
            def rollover_pattern(base_pattern, number):
                if "." in base_pattern:
                    return (base_pattern[:base_pattern.rindex(".")] + "_" +
                            str(number) + base_pattern[base_pattern.rindex("."):])
                else:
                    return base_pattern + "_" + str(number)

        if isinstance(base, file):
            f = base
            base = f.name
        elif isinstance(base, string_types):
            f = None
        else:
            assert False, "base should be an open file or string filename."
        n = 0
        while True:
            if f is None:
                name = rollover_pattern(base, n)
                f = open(name, "wb")
            assert "w" in f.mode
            yield f   # use the first file if given, otherwise start rollover with _0
            f = None  # second file in rollover is always _1 and continuing from there

    @staticmethod
    def _openSingleFile(base):
        if isinstance(base, string_types):
            base = open(base, "wb")
        assert isinstance(base, file) and "w" in base.mode
        return base

    def to_file(self, base, **options):
        """Save this dataset to a file or collection of files.

        base: str or iterable of str
            String file name or iterable of string file names.
        options: optional, of course!
            May contain relevant parameters to pass to the concrete implementation.
        """
        raise NotImplementedError


class AsNumpy(ConvertibleInPlace):
    def asNumpy(self, **options):
        """View this dataset as a NumpyDataset, sharing their underlying data.

        A change in the NumpyDataset modifies the original.
        """
        raise NotImplementedError


class NewNumpy(ConvertibleCopy):
    def newNumpy(self, **options):
        """Copy this dataset into a new NumpyDataset, without sharing any underlying data.

        A change in the NumpyDataset leaves the original untouched.
        """
        raise NotImplementedError


class AsROOT(ConvertibleInPlace):
    def asROOT(self, **options):
        """View this dataset as a ROOTDataset, sharing their underlying data.

        A change in the ROOTDataset modifies the original.
        """
        raise NotImplementedError


class NewROOT(ConvertibleCopy):
    def newROOT(self, **options):
        """Copy this dataset into a new ROOTDataset, without sharing any underlying data.

        A change in the ROOTDataset leaves the original untouched.
        """
        raise NotImplementedError

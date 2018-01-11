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
from ..utils.provenance import FileOrigin, ObjectOrigin, Transformation, Formatting, MultiProvenance, Provenance
from ..dataset.selection import Selection

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
        if isinstance(data, dict):
            self.dicttoarray()
        
        for var in self.data.dtype.names:
            self.__add_var(var)
            
        if isinstance(provenance, MultiProvenance):
            self._provenance = provenance.copy()
        else:
            if provenance is None:
                provenance = ObjectOrigin(repr(data))
            if not isinstance(provenance, ( list, tuple ) ):
                provenance = [provenance]
            
            self._provenance = MultiProvenance(*provenance)
        
    def copy(self) :
        """Get a copy of the NumpyDataset."""
        return NumpyDataset( self.data, self._provenance )
        
    def select(self, selection = None):
        """
        Apply a selection to the NumpyDataset.
        
        Parameters
        ----------
        selection: Selection or str

        Returns
        -------
        new NumpyDataset after selection
        """
  
        if isinstance(selection, numpy.ndarray) and selection.dtype == bool:
            return self.__getitem__(selection)
        elif isinstance(selection, Selection) or isinstance(selection, str):
            if isinstance(selection, str):
                selection = Selection(selection)
                
            data = self.data[ selection.numpyselection(self) ]
            provenance = self._provenance + Transformation("Selection, {}, applied".format(selection))
            return NumpyDataset(data, provenance)
        else:
            raise ValueError("selection input must be of type 'str', 'Selection', or an Array of booleans not {0}".format(type(selection)))
                              
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
        
    def dicttoarray(self):
        """Convert a dictionnary into a structured array."""
        if self.isdictof1d(self.data ) and not self.isrecarray(self.data ):
            dtypes = {'names': self.data .keys(), 'formats': [numpy.dtype(self.data [k].dtype) for k in self.data .keys()]}
            shape  = (len(self.data .values()[0]),)
            array  = numpy.zeros(shape,dtypes)
            
            for k in self.data .keys():
                array[k] = self.data [k]
                
            self._data = array
            
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
            data = numpy.empty(head(self.data.values()).shape,
                               dtype=[(name, self.data[name].dtype) for name in self.data])
            for name in self.data:
                data[name] = self.data[name]
        else:
            assert False, "data must be a Numpy record array or a Python dictionary of 1d Numpy arrays."

        tree = root_numpy.array2tree(self.data, treename)
        from .rootdataset import ROOTDataset
        return ROOTDataset(tree, self.provenance+Formatting('ROOTDataset', treename))

    def __getitem__(self, object):
        
        if isinstance(object, str) and object in self.__dict__.keys():
            array = self.data[object].view(SkhepNumpyArray)
            array.name = object
            array.provenance = ObjectOrigin(repr(self))
            return array.copy()
            # return a copy in order to avoid unrecorded operation due to ndarray mutability
        elif isinstance(object, SkhepNumpyArray) and object.dtype == bool:
            data = self.data[ object ]
            provenance = self.provenance + Transformation("Subsetting dataset: {}".format(object.name), object.name)
            return NumpyDataset(data, provenance)
        else:
            return self.data[object]
                
    def __setattr__(self, name, value):
        listofattributes = self.__dict__.keys()
        
        if isinstance(value, numpy.ndarray) and name != "_data" and name not in listofattributes :
            if value.shape != self.data .shape:
                raise ValueError('Arrays should have the same dimensions')
            else:
                from numpy.lib import recfunctions
                detail = getattr(value, 'provenance', None)
                data = recfunctions.append_fields(self.data , name, value, usemask=False)
                self._data  = data
                self._provenance += Transformation("Array {} has been created".format(name), detail)
                self.__add_var(name)
        else:
            dict.__setattr__(self, name, value)
        
        
    def __setitem__(self, name, array):
        listofattributes = self.__dict__.keys()
        
        if isinstance(array, numpy.ndarray):
            if name not in listofattributes:
                self.__setattr__(name, array)
            elif name != "_data":
                if array.shape != self.data[name].shape:
                    raise ValueError('Arrays should have the same dimensions')
                if isinstance(array, SkhepNumpyArray) and array.provenance[0].detail == repr(self) and array.name == name: 
                    self._data[name] = array.view(numpy.ndarray)
                    self._provenance += MultiProvenance(*array.provenance[1:])                    
                else:
                    array_name = getattr(array, 'name', None)
                    if array_name is None: array_name = repr(array)
                    detail = getattr(array, 'provenance', None)
                    self._data[name] = array
                    self._provenance += Transformation("Array {0} as been replaced by {1}".format(name, array_name), detail)
        else:
            raise ValueError('Not an array!')
                            
    def __add_var(self, var):
        """Add columns of the array as property attributes"""
        def make_get_set(var):
            def getter(self):
                return self.__getitem__(var)
            def setter(self, array):
                self.__setitem__(var, array)
            return getter, setter
                                    
        setattr(NumpyDataset, var, property(*make_get_set(var)))
        self.__dict__[var] = self.data[var]
        
    def __repr__(self):
        """Class representation."""
        return "NumpyDataset{0}".format(repr(self.data).replace("array",""))

    def __str__(self):
        """Simple class representation."""
        return str(self.data)
    
        
# -----------------------------------------------------------------------------
# SkhepNumpyArray
# -----------------------------------------------------------------------------
            
class SkhepNumpyArray(numpy.ndarray):
    def __new__(cls, inputarray, name=None, provenance=None):
        """Default constructor for SkhepNumpyArray.

        Parameters
        ----------
        input_array: numpy array, list or tuple.
        name: name of the variable.
        provenance: history of the variable.
        """
                
        instance = numpy.asarray(inputarray).view(cls)
        instance._name  = name
        
        if isinstance(provenance, MultiProvenance):
            instance._provenance = provenance.copy()
        else:
            if provenance is None:
                provenance = ObjectOrigin(repr(inputarray))
            if not isinstance(provenance, ( list, tuple ) ):
                provenance = [provenance]
            instance._provenance = MultiProvenance(*provenance)
            
        return instance
     
    @inheritdoc(numpy.ndarray)    
    def __array_finalize__(self, obj):        
        if obj is None: return
        self._name = getattr(obj, 'name', None)
        self._provenance = getattr(obj, 'provenance', MultiProvenance(ObjectOrigin(repr(obj))))
                
        
    def copy(self):
        """Get a copy of the SkhepNumpyArray."""
        return SkhepNumpyArray(numpy.copy(self), name = self._name, provenance = self._provenance)
                        
    @property
    def name(self):
        """Return the name of the variable inside the SkhepNumpyArray."""
        return self._name
        
    @property
    def provenance(self):
        """Return the provenance of the SkhepNumpyArray."""
        return self._provenance
        
    @provenance.setter
    def provenance(self, provenance):
        """Sets the provenance of the SkhepNumpyArray."""
        if isinstance(provenance, MultiProvenance):
            self._provenance = provenance
        elif isinstance(provenance, Provenance):
            self._provenance = MultiProvenance(provenance)
        else:
            raise NotImplementedError
        
    @name.setter
    def name(self, name):
        """Sets the name of the variable inside the SkhepNumpyArray."""
        self._name = name
     
    @inheritdoc(numpy.ndarray)   
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
               
        args = []
        names_input = []
        for _input in inputs:
            if hasattr(_input, "name"):
                names_input.append(_input.name)
            else:
                names_input.append(repr(_input))
            args.append(numpy.asarray(_input))
                
        outputs = kwargs.pop('out', None)
        if outputs:
            out_args = []
            for o in outputs:
                out_args.append(numpy.asarray(o))
            kwargs['out'] = tuple(out_args)
            
        name       = self.name
        provenance = self.provenance
        result = getattr(ufunc, method)(*args, **kwargs)
    
        if ufunc != numpy.logical_and and ufunc != numpy.logical_or:
            result = result.view(SkhepNumpyArray)
            
            #min max
            if ufunc == numpy.maximum or ufunc == numpy.minimum:
                if ufunc == numpy.maximum:
                    name = "max("
                if ufunc == numpy.maximum:
                    name = "min("
                
                for ni in names_input:
                    if ni == names_input[-1]:
                        name += " {} )".format(ni)
                    else:
                        name += " {},".format(ni)

                provenance = ObjectOrigin(name) 
                
            #comparison operators
            comparisaton_operators = {"<ufunc 'greater'>": ">", "<ufunc 'less'>": "<", "<ufunc 'greater_equal'>": ">=", "<ufunc 'less_equal'>": "<=",
                    "<ufunc 'equal'>": "==", "<ufunc 'not_equal'>": "!=", "<ufunc 'bitwise_and'>": "&", "<ufunc 'bitwise_or'>": "|"}
            
            if str(ufunc) in comparisaton_operators.keys():
                op = comparisaton_operators[str(ufunc)]
                lhs = names_input[0]
                rhs = names_input[1]
                
                if op == "&" or op == "|":
                    lhs = "("+lhs+")"
                    rhs = "("+rhs+")"
                
                name = "{0} {1} {2}".format(lhs, op, rhs)
                provenance = ObjectOrigin(name)
                
            #arithmetic operators
            arithmetic_operators = {"<ufunc 'add'>": "+", "<ufunc 'subtract'>": "-", "<ufunc 'multiply'>": "*", "<ufunc 'divide'>": "/",
                        "<ufunc 'power'>": "^"}
            
            if ufunc == numpy.square:
                name = "{0}^2".format(names_input[0])
                provenance = ObjectOrigin(name)
                
            if str(ufunc) in arithmetic_operators.keys():
                op = arithmetic_operators[str(ufunc)]
                lhs = names_input[0]
                rhs = names_input[1]
                
                # __add__
                if op == "+":
                    provenance += Transformation("{1} as been added to {0}".format(lhs, rhs))
                # __sub__
                elif op == "-":
                    provenance += Transformation("{1} as been subtracted to {0}".format(lhs, rhs))
                # __mul__
                elif op == "*":
                    provenance += Transformation("{0} as been multiplied by {1}".format(lhs, rhs))
                # __mul__
                elif op == "/":
                    provenance += Transformation("{0} as been divided by {1}".format(lhs, rhs))
                    
                if outputs is None:
                                            
                    name = "({0}) {1} ({2})".format(lhs, op, rhs)
                
                            
            if isinstance(result, SkhepNumpyArray):
                result.name       = name
                result.provenance = provenance
            
        return result
# -----------------------------------------------------------------------------
# Add Numpy methods to NumpyDataset in bulk.
# -----------------------------------------------------------------------------
#def addNumpyMethod(method):
#    def fn(self, name, *args, **kwds):
#        return method.__call__(self.data, *args, **kwds)
#
#    fn.__name__ = method.__name__
#    fn.__doc__ = method.__doc__
#    if sys.version_info[0]==2:  # ugly but works! TODO: find nicer way
#        setattr(NumpyDataset, method.__name__, MethodType(fn, None, NumpyDataset))
#    else:
#        setattr(NumpyDataset, method.__name__, MethodType(fn, NumpyDataset))
#
#try:
#    addNumpyMethod(numpy.ndarray.__add__)
#    addNumpyMethod(numpy.ndarray.__mul__)
#    addNumpyMethod(numpy.ndarray.sum)
#    addNumpyMethod(numpy.ndarray.mean)
#except ImportError:
#    pass

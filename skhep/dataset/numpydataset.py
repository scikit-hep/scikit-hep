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
        
    def copy(self):
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
          
          nbefore    = self.nevents 
          nafter     = len(data)
          efficiency = float( nafter / nbefore )
          error      = (( efficiency * ( 1. - efficiency ) ) / nbefore ) ** 0.5
          
          tr_name    = "Selection, {0}, applied".format(selection)
          tr_detail1 = "#events before = {0}".format(nbefore)
          tr_detail2 = "#events after = {0}".format(nafter)
          tr_detail3 = "Efficiency = {0:.4f} +/- {1:.4f} %".format(efficiency * 100, error * 100)
          
          provenance = self._provenance + Transformation(tr_name, tr_detail1, tr_detail2, tr_detail3)
          return NumpyDataset(data, provenance)
          
        else:
          raise ValueError("selection input must be of type 'str', 'Selection', or an Array of booleans not {0}".format(type(selection)))
    
    @property        
    def nevents(self):
        """Get the number of events in the NumpyDataset."""
        return self.__len__()
     
    @property   
    def nentries(self):
        """Get the number of entries in the NumpyDataset. Same as 'nevents'"""
        return self.__len__()
        
    @property        
    def variables(self):
      """
      Get the list of variables in the NumpyDataset, i.e. the content of 'numpy.dtype.names'
      of the stored NumPy array.
      """
      return [var for var in self.data.dtype.names]
      
    def keys(self):
      """
      Get the list of keys in the NumpyDataset, same as 'variables'
      """
      return [var for var in self.data.dtype.names]
                              
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
        """Convert a dictionnary into a structured array. If using Python3, byte keys are
        decoded into string.
        """
        if self.isdictof1d(self.data ) and not self.isrecarray(self.data ):
            if sys.version_info[0] > 2 and any(isinstance(k, bytes) for k in self.data.keys()):
              data = {}
              for k in list(self.data.keys()):
                if isinstance(k, bytes):
                  data[k.decode()] = self.data[k]
                else:
                  data[k] = self.data[k]
            else:
              data = self.data
          
            dtypes = {'names': list(data.keys()), 'formats': [numpy.dtype(self.data [k].dtype) for k in self.data .keys()]}
            shape  = (len(list(self.data .values())[0]),)
            array  = numpy.zeros(shape,dtypes)
            
            for k in data.keys():
                array[k] = data[k]
                
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
        data = dict((name, self.data[name])
                    for name in self.data.dtype.names)
                    
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
            provenance = self.provenance + Transformation("Subsetting dataset: {0}".format(object.name), object.name)
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
                self._provenance += Transformation("Array {0} has been created".format(name), detail)
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
                    self._provenance += Transformation("Array {0} has been replaced by {1}".format(name, array_name), detail)
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
        
    def __len__(self):
        return len(self.data)
 

def can_override_ufunc ( ):
    # check whether or not __array_ufunc__ can be overidden
    # possible for numpy version > 1.13
    
    version = numpy.__version__
    version = version.split(".")
    version = [int(v) for v in version]
    return version[0] >= 1. and version[1] >= 13.   
        
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
        self._provenance = getattr(obj, 'provenance', MultiProvenance(ObjectOrigin("")))
        
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
            raise ValueError("Inputs must be Provenance types!")
        
    @name.setter
    def name(self, name):
        """Sets the name of the variable inside the SkhepNumpyArray."""
        self._name = name
        
        
    @inheritdoc(numpy.ndarray)   
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        args = []
        names_inputs = []
        for _input in inputs:
            if hasattr(_input, "name"):
                names_inputs.append(_input.name)
            else:
                names_inputs.append(repr(_input))
            array_input =  numpy.asarray(_input)   
            if ufunc == numpy.divide:
                array_input = array_input.astype(float)
            args.append(array_input)
         
        outputs = kwargs.pop('out', None)       
        if outputs is not None:
            out_args = []
            for o in outputs:
                array_out = numpy.asarray(o)
                if ufunc == numpy.divide:
                    array_out = array_out.astype(float)
                out_args.append(array_out)
            kwargs['out'] = tuple(out_args)
                    
        name       = self.name
        provenance = self.provenance.copy()
        result     = getattr(ufunc, method)(*args, **kwargs)
    
        if method != "at":
          result = result.view(SkhepNumpyArray)
          result = self.__format_ufunc_result( provenance, result, ufunc, names_inputs, outputs)
          return result
        
    def __format_ufunc_result(self, provenance, result, ufunc, names_inputs, outputs = None):

        #comparisaton_operators    
        comparisaton_operators = {"<ufunc 'greater'>": ">", "<ufunc 'less'>": "<", 
                                  "<ufunc 'greater_equal'>": ">=", "<ufunc 'less_equal'>": "<=",
                                  "<ufunc 'equal'>": "==", "<ufunc 'not_equal'>": "!=", 
                                  "<ufunc 'bitwise_and'>": "&", "<ufunc 'bitwise_or'>": "|"}
            
        #arithmetic operators                              
        arithmetic_operators =   {"<ufunc 'add'>": "+", "<ufunc 'subtract'>": "-", 
                                  "<ufunc 'multiply'>": "*", "<ufunc 'divide'>": "/", 
                                  "<ufunc 'true_divide'>": "/", "<ufunc 'power'>": "^"}
                    
        functions = {"<ufunc 'mininum'>": "min", "<ufunc 'maximum'>": "max", "<ufunc 'sin'>": "sin", 
                     "<ufunc 'sin'>": "cos", "<ufunc 'tan'>": "tan", "<ufunc 'arcsin'>": "arcsin", 
                     "<ufunc 'arccos'>": "arccos", "<ufunc 'arctan'>": "arctan",
                     "<ufunc 'arctan2'>": "arctan2", "<ufunc 'sinh'>": "sinh", "<ufunc 'cosh'>": "cosh",
                     "<ufunc 'tanh'>": "tanh", "<ufunc 'arcsinh'>": "arcsinh",
                     "<ufunc 'arccosh'>": "arcosh", "<ufunc 'log'>": "log", "<ufunc 'log10'>": "log10",
                     "<ufunc 'log1p'>": "log1p", "<ufunc 'exp'>": "exp", "<ufunc 'expm1'>": "expm1", 
                     "<ufunc 'absolute'>": "abs"}
                                   
        if ufunc != numpy.logical_and and ufunc != numpy.logical_or:
                            
            #comparisaton_operators
            if str(ufunc) in comparisaton_operators.keys():
              name, provenance = self.__comparison_ufunc( comparisaton_operators[str(ufunc)], provenance, names_inputs)
                
            #functions
            elif str(ufunc) in functions.keys():
              name, provenance = self.__function_ufunc( functions[str(ufunc)], provenance, names_inputs)
                                               
            #arithemtic_operators
            elif ufunc == numpy.square:
              name, provenance = self.__square_ufunc( provenance, outputs)
              
            elif ufunc == numpy.sqrt:
              name, provenance = self.__sqrt_ufunc( provenance, outputs)
            
            elif str(ufunc) in arithmetic_operators.keys():
              name, provenance = self.__arithmetic_ufunc( arithmetic_operators[str(ufunc)], provenance, names_inputs, outputs)
                
            else:
                
                name, provenance = self.name, self.provenance
                   
            if isinstance(result, SkhepNumpyArray):
                result.name       = name
                result.provenance = provenance
                
        return result
        
    def __function_ufunc( self, function, provenance, names_inputs):
      
      name = function + "("
      
      for ni in names_inputs:
        if ni == names_inputs[-1]:
          name += " {0} )".format(ni)
        else:
          name += " {0},".format(ni)
          
      provenance += Transformation(name)

      return name, provenance
      
    def __comparison_ufunc( self, operator, provenance, names_inputs ):
        lhs = names_inputs[0]
        rhs = names_inputs[1]

        if operator == "|":
            lhs = "("+lhs+")"
            rhs = "("+rhs+")"
        
        name = "{0} {1} {2}".format(lhs, operator, rhs)
        provenance = ObjectOrigin(name)
        return name, provenance
        
    def __format_operand( self, operand, operator):
        if operator == "*"   and any( _op in operand for _op in ["+","-","/"]):
            operand = "({0})".format( operand )
        elif operator == "/" and any( _op in operand for _op in ["+","-","*"]):
            operand = "({0})".format( operand )
        elif operator == "^" and any( _op in operand for _op in ["+","-","*","/"]):
            operand = "({0})".format( operand )

        return operand
        
    def __square_ufunc( self, provenance, outputs = None):
        
        name_input = self.name
        
        provenance += Transformation("{0} has been squared".format(name_input))
        
        if outputs is None:
            name_input = self.__format_operand( name_input, "^")
            name = "{0}**2".format(name_input)
        else:
            name = self.name
            
        return name, provenance
        
    def __sqrt_ufunc( self, provenance, outputs = None):
      
        name_input = self.name
        
        provenance += Transformation("{0} has been raised to the power of 0.5".format(name_input))
        
        if outputs is None:
          name_input = self.__format_operand( name_input, "^")
          name = "{0}**0.5".format(name_input)
        else:
          name = self.name
          
        return name, provenance
        
    def __arithmetic_ufunc( self, operator, provenance, names_inputs, outputs = None):
        lhs = names_inputs[0]
        rhs = names_inputs[1]
        
        # __add__
        if operator == "+":
            provenance += Transformation("{1} has been added to {0}".format(lhs, rhs))
        # __sub__
        elif operator == "-":
            provenance += Transformation("{1} has been subtracted to {0}".format(lhs, rhs))
        # __mul__
        elif operator == "*":
            provenance += Transformation("{0} has been multiplied by {1}".format(lhs, rhs))
        # __mul__
        elif operator == "/":
            provenance += Transformation("{0} has been divided by {1}".format(lhs, rhs))
        # power
        elif operator == "^":
            provenance += Transformation("{0} has been raised to the power of {1}".format(lhs, rhs))
        
        if outputs is None:
            lhs = self.__format_operand(lhs, operator)
            rhs = self.__format_operand(rhs, operator)
            if operator == "^":
                name = "{0}{1}{2}".format(lhs, operator, rhs)
            else:
                name = "{0} {1} {2}".format(lhs, operator, rhs)
        else:
            name = self.name
                    
        return name, provenance
                
    ### overloading operators in case numpy version < 1.13, will 
      
    if not can_override_ufunc():
        
        __array_priority__ = 2.0
                
        @inheritdoc(numpy.ndarray) 
        def __array_wrap__(self, array, context=None):
            
            if context:
                _context = list(context)
                ufunc  = _context[0]
                inputs = _context[1]
                
                names_inputs = []
                for i in inputs:
                    names_inputs.append( getattr(i, 'name', repr(i)) )
                
                provenance = self.provenance.copy()
                array.view(SkhepNumpyArray)
                
                array = self.__format_ufunc_result( provenance, array, ufunc, names_inputs)
                
            return array
                    
        def __iadd__(self, other):
            return self.__array_ufunc__(numpy.add, "__call__", self, other, out=(self,))
 
        def __isub__(self, other):
            return self.__array_ufunc__(numpy.subtract, "__call__", self, other, out=(self,))
            
        def __imul__(self, other):
            return self.__array_ufunc__(numpy.multiply, "__call__", self, other, out=(self,))
      
        def __idiv__(self, other):
            return self.__array_ufunc__(numpy.divide, "__call__", self, other, out=(self,))
            
        def __itruediv__(self, other):
            return self.__array_ufunc__(numpy.true_divide, "__call__", self, other, out=(self,))
            
        def __pow__(self, other):
            if isinstance(other, (int, float)) and other == 2.0:
                return self.__array_ufunc__(numpy.square, "__call__", self)
            else:
                return self.__array_ufunc__(numpy.power, "__call__", self, other)
                
        def __ipow__(self, other):
            if isinstance(other, (int, float)) and other == 2.0:
                return self.__array_ufunc__(numpy.square, "__call__", self, out=(self,))
            else:
                ufunc = numpy.power
                return self.__array_ufunc__(numpy.power, "__call__", self, other, out=(self,))
                



# -----------------------------------------------------------------------------
# Add Numpy methods to NumpyDataset in bulk.
# SkhepNumpyArray
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
#  try:
#     addNumpyMethod(numpy.ndarray.__add__)
#     addNumpyMethod(numpy.ndarray.__mul__)
#     addNumpyMethod(numpy.ndarray.sum)
#     addNumpyMethod(numpy.ndarray.mean)
#  except ImportError:
#    pass
            
        
        
    
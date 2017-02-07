# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Module for backends
===================

The following backends are supported in Scikit-HEP:
* ROOT
* NumPy
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import, print_function

__all__ = [ 'backends', 'backend_converter_mapping' ]


#-----------------------------------------------------------------------------
# Utilities providing information on supported backends and converters
#-----------------------------------------------------------------------------
# Set of supported backends
backends_supported = ( 'root', 'numpy' )

def backends():
    print( 'Available backends (all names stored in lowercase):' )
    print( ' '.join(backends_supported) )

def backend_converter_mapping():
    """
    Print a matrix of converters among all available backends.
    """
    m = """
    Converters implemented for the supported backends:
    
      ROOT          NumPy
      -----------------------------------
      TTree   <->   Structured array
    """
    print(m)

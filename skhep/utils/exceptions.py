# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Submodule for useful exceptions
===============================

.. note:: not meant for user code in general, though possible.
"""

# Definition of handy colours for printing
_default = '\x1b[00m'
_green   = '\x1b[01;32m'
_red     = '\x1b[01;31m'

class InvalidOperationError(Exception):
    """Exception class for meaningless operations."""
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
    def __str__(self):
        """String representation."""
        return ( _red + self.message + _default )

class SkhepTypeError(Exception):
    """Exception class for non-instantiable classes."""
    def __init__(self,name):
        Exception.__init__(self,name)
        self.message = "'{0}' is an abstract base class. Instantiate one of its subclasses instead.".format(name)
    def __str__(self):
        """String representation."""
        return ( _red + self.message + _default )

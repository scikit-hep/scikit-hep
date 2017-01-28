# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Module for Scikit-HEP exceptions
================================

List of exceptions defined:
* NotSupportedBackendError: for backends not (yet) supported.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

__all__ = [ 'NotSupportedBackendError' ]


#-----------------------------------------------------------------------------
# Definition of available exceptions
#-----------------------------------------------------------------------------
class NotSupportedBackendError( NotImplementedError ):
    """
    Exception class representing a backend not (yet) implemented.
    """
    def __init__( self, location, msg ):
        self.location, self.msg = location, msg
    
    def __str__( self ):
        return "[%s] %s" % ( self.location, self.msg )

# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Submodule for useful exceptions
===============================
"""

class InvalidOperationError(Exception):
    """
    Exception class for meaningless operations.
    """
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
    

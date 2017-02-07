# Licensed under a 3-clause BSD style license, see LICENSE.
"""
***********************************
Subpackage for converters to Pandas
***********************************

"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from skhep.exceptions import NotSupportedBackendError

__all__ = [ 'tree2df' ]


#-----------------------------------------------------------------------------
# Definition of available converters
#-----------------------------------------------------------------------------
def tree2df( ttree ):
    """Converter a TTtree to a DataFrame."""
    raise NotSupportedBackendError( __name__, 'Pandas converters not yet available!')

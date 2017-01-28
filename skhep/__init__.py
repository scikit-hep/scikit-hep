# Licensed under a 3-clause BSD style license, see LICENSE.
"""
   _____      _ _    _ _          _    _ ______ _____
  / ____|    (_) |  (_) |        | |  | |  ____|  __ \ 
 | (___   ___ _| | ___| |_  ____ | |__| | |__  | |__) | 
  \___ \ / __| | |/ / | __| ____ |  __  |  __| |  ___/ 
  ____) | (__| |   <| | |_       | |  | | |____| | 
 |_____/ \___|_|_|\_\_|\__|      |_|  |_|______|_|      {0}

A community-driven and oriented Python software project for High Energy Physics.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

# Information on supported backends
from .backends import *

# Set of scikit-hep exceptions
from .exceptions import *


#-----------------------------------------------------------------------------
# Project and package info
#-----------------------------------------------------------------------------
__version__ = '0.0.1'

project_url        = 'http://scikit-hep.org'
project_url_GitHub = 'https://github.com/scikit-hep/scikit-hep'
project_url_PyPI   = 'https://pypi.python.org/pypi/scikit-hep'

__doc__ = __doc__.format( __version__ )

banner = __doc__

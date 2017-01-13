# Licensed under a 3-clause BSD style license, see LICENSE.
"""
  .-.          .         .        .   ..---..--. 
 (   )      o  |      o _|_       |   ||    |   )
  `-.  .-.  .  |.-.   .  |   ____ |---||--- |--' 
 (   )(     |  |-.'   |  |        |   ||    |    
  `-'  `-'-' `-'  `--' `-`-'      '   ''---''      {0}

A community-driven and oriented Python software project for High Energy Physics.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

__all__ = [ 'banner',
            'project_url',
            'project_url_GitHub',
            'project_url_PyPI'
            ]

#-----------------------------------------------------------------------------
# Project and package info
#-----------------------------------------------------------------------------
__version__ = '0.0.1'

__doc__ = __doc__.format( __version__ )

banner = __doc__

project_url        = 'http://scikit-hep.org'
project_url_GitHub = 'https://github.com/scikit-hep/scikit-hep'
project_url_PyPI   = 'https://pypi.python.org/pypi/scikit-hep'

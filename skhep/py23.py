# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Trivial module to deal with Python 2 and 3 compatibility.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import sys


#-----------------------------------------------------------------------------
# Python 2 and 3 "conversions"
#-----------------------------------------------------------------------------
if sys.version_info[0] > 2:
    string_types = (bytes, str)
    xrange = range
    long = int
else:
    string_types = (str, unicode)

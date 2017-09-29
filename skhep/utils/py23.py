# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Trivial module to deal with Python 2 and 3 compatibility.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import sys

# -----------------------------------------------------------------------------
# Python 2 and 3 "conversions"
# -----------------------------------------------------------------------------
if sys.version_info[0] > 2:
    string_types = (bytes, str)
    xrange = range
    long = int
    from io import IOBase
    file = IOBase


    def head(x):
        return iter(x).__next__()

else:
    string_types = (str, unicode)


    def head(x):
        return iter(x).next()

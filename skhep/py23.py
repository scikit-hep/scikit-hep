# Licensed under a 3-clause BSD style license, see LICENSE.
"""
___  __ .    . ___       ___ ___
|_  |   | |/ |  |  _ |_| |_  |_|
__| |__ | |\ |  |    | | |__ |     {0}

A community-driven and oriented Python software project for High Energy Physics.
"""

import sys

if sys.version_info[0] > 2:
    string_types = (bytes, str)
    xrange = range
    long = int
else:
    string_types = (str, unicode)

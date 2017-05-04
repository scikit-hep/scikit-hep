#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.math.vectors import *
from skhep.utils.py23 import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_vectors_constructors()
    
    def test_vectors_constructors(self):
        v1 = Vector3D()
        self.assertEqual( str(v1), str((0.,0.,0.)) )

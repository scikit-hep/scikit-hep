#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.math import *
from skhep.util.py23 import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_kinematics()
    
    def test_kinematics(self):
        self.assertEqual( Kallen_function(2,1,0), 1)

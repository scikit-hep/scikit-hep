#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.math.kinematics module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import unittest

from skhep.math.kinematics import *
from skhep.units import GeV, ps
from skhep.constants import hbar
from skhep.utils.py23 import *


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_kinematics_Kallen_function()
        self.test_width_lifetime_conversions()
    
    def test_kinematics_Kallen_function(self):
        self.assertEqual(Kallen_function(2, 1, 0), 1)
    
    def test_width_lifetime_conversions(self):
        self.assertAlmostEqual(lifetime_to_width(1.5*ps)/GeV,4.388079676311604e-13)
        self.assertTrue(1.5*ps * lifetime_to_width(1.5*ps) == hbar)
        self.assertTrue(width_to_lifetime(hbar) == 1 * MeV)
        #
        self.assertRaises(ValueError, lifetime_to_width, -1)
        self.assertRaises(ValueError, width_to_lifetime, -1)

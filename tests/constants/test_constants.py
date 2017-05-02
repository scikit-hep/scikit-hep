#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the constants.constants module.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.constants import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_constants()

    def test_constants(self):
        self.assertEqual( c_light / (m/s), 299792458 )
        self.assertAlmostEqual( hbarc_sq / c_light_sq, (h_Planck/two_pi)**2 )

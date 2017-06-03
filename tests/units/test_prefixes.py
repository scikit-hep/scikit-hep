#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.units.prefixes module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import unittest

from math import log

from skhep.units import mega, micro, yotta, yocto, kibi, tebi


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_prefixes_e6()
        self.test_prefixes_e24()

    def test_prefixes_e6(self):
        self.assertEqual(4 * mega, 1. / 0.25 / micro)

    def test_prefixes_e24(self):
        self.assertAlmostEqual(yotta * yocto, 1.)

    def test_prefixes_binary(self):
        self.assertEqual(log(kibi, 2), 10)
        self.assertEqual(log(tebi, 2), 40)

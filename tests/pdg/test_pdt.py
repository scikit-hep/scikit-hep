#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.pdg import *
from skhep.utils.py23 import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_pdt()

    def test_pdt(self):
        tbl = ParticleDataTable('skhep/data/mass_width_2016.mcd')
        self.assertEqual(tbl('f(0)(500)0').name,tbl[9000221].name)
        self.assertEqual(tbl('f(0)(500)0').id,9000221)
        self.assertTrue(tbl.has_key(11))
        self.assertTrue(tbl.has_particle(2212))
        self.assertEqual(tbl.particle(21).__repr__(),'g0: ID=21, m=0 GeV, 3*q=0, width=0 GeV')

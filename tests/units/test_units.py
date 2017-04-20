#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.units import *
from skhep.utils.py23  import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_length()
        self.test_area()
        self.test_crosssection()
        self.test_volume()
        self.test_time()
        self.test_frequency()
        self.test_energy()

    def test_length(self):
        self.assertAlmostEqual(3 * mm, m * 0.003)
        self.assertAlmostEqual(3 * mm, cm * 0.3)
        self.assertAlmostEqual(3 * mm, km * 0.000003)
        self.assertAlmostEqual(3 * mm, micrometer * 3000)
        self.assertAlmostEqual(3 * mm, nanometer * 3000000)
        self.assertAlmostEqual(3 * mm, angstrom * 30000000)
        self.assertAlmostEqual(3 * mm, fermi * 3e12)
        self.assertAlmostEqual(100 * fm2, barn)

    def test_area(self):
        self.assertAlmostEqual((3 * mm)**2, 9 * mm2)
        self.assertAlmostEqual((3 * cm)**2, 9 * cm2)
        self.assertAlmostEqual((3 * km)**2, 9 * km2)
        self.assertAlmostEqual(2e-28 * meter2, 2 * barn)

    def test_crosssection(self):
        self.assertAlmostEqual(3e-31 * barn, 9 * millibarn)
        self.assertAlmostEqual(3e-34 * barn, 9 * microbarn)
        self.assertAlmostEqual(3e-37 * barn, 9 * nanobarn)
        self.assertAlmostEqual(3e-40 * barn, 9 * picobarn)
        self.assertAlmostEqual(1 * barn, 100 * fm2)

    def test_volume(self):
        self.assertAlmostEqual((3 * mm)**3, 27 * mm3)
        self.assertAlmostEqual((3 * cm)**3, 27 * cm3)
        self.assertAlmostEqual((3 * m)**3, 27 * m3)

    def test_time(self):
        self.assertAlmostEqual(3 * ns, 3e-9 * s)
        self.assertAlmostEqual(3 * ns, 3e-6 * ms)
        self.assertAlmostEqual(3 * ns, 3e-3 * microsecond)
        self.assertAlmostEqual(3 * ns, 3000 * picosecond)
        self.assertAlmostEqual(3 * ns, 3000000 * femtosecond)

    def test_frequency(self):
        self.assertAlmostEqual(second**-1, Hz)
        self.assertAlmostEqual(1000 * hertz, kHz)
        self.assertAlmostEqual(1000000 * hertz, MHz)
        self.assertAlmostEqual(1000000000 * hertz, GHz)

    def test_energy(self):
        self.assertAlmostEqual(1e3 * eV, keV)
        self.assertAlmostEqual(1e6 * eV, MeV)
        self.assertAlmostEqual(1e9 * eV, GeV)
        self.assertAlmostEqual(1e12 * eV, TeV)
        self.assertAlmostEqual(1e15 * eV, PeV)
        self.assertAlmostEqual(1e18 * eV, EeV)

    def test_magnetic_field(self):
        self.assertAlmostEqual(10 * gauss, 1 * milli * tesla)

    def test_electricity(self):
        self.assertAlmostEqual(1 * mega * joule / second, 1 * MW)

    def test_radiation_units(self):
        self.assertEqual(gray, sievert)  # equal in terms of value
        self.assertEqual( 1 * curie, 37 * giga * becquerel)

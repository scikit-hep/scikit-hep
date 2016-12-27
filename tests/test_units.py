#!/usr/bin/env python

# Copyright 2016 DIANA-HEP
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from skhep.units import *

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
        self.assertEqual(3 * mm, m * 0.003)
        self.assertEqual(3 * mm, cm * 0.03)
        self.assertEqual(3 * mm, km * 0.000003)
        self.assertEqual(3 * mm, micrometer * 3000)
        self.assertEqual(3 * mm, nanometer * 3000000)
        self.assertEqual(3 * mm, angstrom * 30000000)
        self.assertEqual(3 * mm, fermi * 3000000000)

    def test_area(self):
        self.assertEqual((3 * mm)**2, 9 * mm2)
        self.assertEqual((3 * cm)**2, 9 * cm2)
        self.assertEqual((3 * km)**2, 9 * km2)
        self.assertEqual(2e-28 * meter2, 2 * barn)

    def test_crosssection(self):
        self.assertEqual(3e-31 * barn, 9 * millibarn)
        self.assertEqual(3e-34 * barn, 9 * microbarn)
        self.assertEqual(3e-37 * barn, 9 * nanobarn)
        self.assertEqual(3e-40 * barn, 9 * picobarn)

    def test_volume(self):
        self.assertEqual((3 * mm)**3, 27 * mm3)
        self.assertEqual((3 * cm)**3, 27 * cm3)
        self.assertEqual((3 * m)**3, 27 * m3)

    def test_time(self):
        self.assertEqual(3 * ns, 3e9 * s)
        self.assertEqual(3 * ns, 3e6 * ms)
        self.assertEqual(3 * ns, 3e3 * microsecond)
        self.assertEqual(3 * ns, 0.003 * picosecond)
        self.assertEqual(3 * ns, 0.000003 * femtosecond)

    def test_frequency(self):
        self.assertEqual(second**-1, Hz)
        self.assertEqual(1000 * hertz, kHz)
        self.assertEqual(1000000 * hertz, MHz)
        self.assertEqual(1000000000 * hertz, GHz)

    def test_energy(self):
        self.assertEqual(1e3 * eV, keV)
        self.assertEqual(1e6 * eV, MeV)
        self.assertEqual(1e9 * eV, GeV)
        self.assertEqual(1e12 * eV, TeV)
        self.assertEqual(1e15 * eV, PeV)
        self.assertEqual(1e18 * eV, EeV)

    # no integrated luminosity???


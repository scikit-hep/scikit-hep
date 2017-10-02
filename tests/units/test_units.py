#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.units.units module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from skhep.units import *
from skhep.constants import two_pi
from skhep.utils.py23 import *
from pytest import approx


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_length():
    assert 3 * mm == approx(m * 0.003)
    assert 3 * mm == approx(cm * 0.3)
    assert 3 * mm == approx(km * 0.000003)
    assert 3 * mm == approx(micrometer * 3000)
    assert 3 * mm == approx(nanometer * 3000000)
    assert 3 * mm == approx(angstrom * 30000000)
    assert 3 * mm == approx(fermi * 3e12)

def test_area():
    assert (3 * mm) ** 2 == approx(9 * mm2)
    assert (3 * cm) ** 2 == approx(9 * cm2)
    assert (3 * km) ** 2 == approx(9 * km2)
    assert 2e-28 * meter2 == approx(2 * barn)

def test_crosssection():
    assert 3e-31 * barn == approx(9 * millibarn)
    assert 3e-34 * barn == approx(9 * microbarn)
    assert 3e-37 * barn == approx(9 * nanobarn)
    assert 3e-40 * barn == approx(9 * picobarn)
    assert 1 * barn == approx(100 * fm2)

def test_luminosity():
    assert invpb / invfb == approx(1.e-3)

def test_volume():
    assert (3 * mm) ** 3 == approx(27 * mm3)
    assert (3 * cm) ** 3 == approx(27 * cm3)
    assert (3 * m) ** 3 == approx(27 * m3)

def test_time():
    assert 3 * ns == approx(3e-9 * s)
    assert 3 * ns == approx(3e-6 * ms)
    assert 3 * ns == approx(3e-3 * microsecond)
    assert 3 * ns == approx(3000 * picosecond)
    assert 3 * ns == approx(3000000 * femtosecond)
    assert day == 24 * 60 * minute

def test_frequency():
    assert second ** -1 == approx(Hz)
    assert 1000 * hertz == approx(kHz)
    assert 1000000 * hertz == approx(MHz)
    assert 1000000000 * hertz == approx(GHz)

def test_energy():
    assert 1e3 * eV == approx(keV)
    assert 1e6 * eV == approx(MeV)
    assert 1e9 * eV == approx(GeV)
    assert 1e12 * eV == approx(TeV)
    assert 1e15 * eV == approx(PeV)
    assert 1e18 * eV == approx(EeV)

def test_angle():
    assert 360. * degree == two_pi * radian

def test_magnetic_field():
    assert 10 * gauss == approx(1 * milli * tesla)

def test_electricity():
    assert 1 * mega * joule / second == approx(1 * MW)

def test_radiation_units():
    assert gray == sievert  # equal in terms of value
    assert 1 * curie == 37 * giga * becquerel

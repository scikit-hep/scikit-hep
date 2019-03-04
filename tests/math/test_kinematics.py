#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.math.kinematics module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest
from pytest import approx

from hepunits.units import GeV, ps
from hepunits.constants import hbar

from skhep.math.kinematics import *
from skhep.math.vectors import Vector3D
from skhep.utils.py23 import *

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_kinematics_Kallen_function():
    assert Kallen_function(2, 1, 0) == 1

def test_valid_Armenteros_Podolanski_variables():
    d1 = Vector3D(1., 2., 3.)
    d2 = Vector3D(1., -2., 3.)
    assert Armenteros_Podolanski_variables(d1, d2) == (2.0, 0.0)

def test_invalid_Armenteros_Podolanski_variables():
    d1 = Vector3D(1., 2., 3.)
    d2 = Vector3D(-1., -2., -3.)
    with pytest.raises(ValueError):
        Armenteros_Podolanski_variables(d1, d2)

def test_width_lifetime_conversions():
    assert lifetime_to_width(1.5*ps)/GeV == approx(4.388079676311604e-13)
    assert 1.5*ps * lifetime_to_width(1.5*ps) == hbar
    assert width_to_lifetime(hbar) == 1 * MeV
    #
    with pytest.raises(ValueError):
        lifetime_to_width(-1)
    with pytest.raises(ValueError):
        width_to_lifetime(-1)

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

from skhep.math.kinematics import *
from skhep.units import GeV, ps
from skhep.constants import hbar
from skhep.utils.py23 import *

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_kinematics_Kallen_function():
    assert Kallen_function(2, 1, 0) == 1

def test_width_lifetime_conversions():
    assert lifetime_to_width(1.5*ps)/GeV == approx(4.388079676311604e-13)
    assert 1.5*ps * lifetime_to_width(1.5*ps) == hbar
    assert width_to_lifetime(hbar) == 1 * MeV
    #
    with pytest.raises(ValueError):
        lifetime_to_width(-1)
    with pytest.raises(ValueError):
        width_to_lifetime(-1)

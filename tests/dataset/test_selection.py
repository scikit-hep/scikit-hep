#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.dataset.selection module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest
import os

import numpy as np

from skhep.utils.provenance import ObjectOrigin  # these are not imported automatically
from skhep.dataset.numpydataset import *
from skhep.dataset.selection import Selection


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_constructors():
	s = Selection()

def test_methods():
	s1 = Selection("x > 1")
	assert s1.__repr__() == "x > 1"
	assert s1.parsed.lhs == "x"
	assert s1.parsed.operator == ">"
	assert s1.parsed.rhs == "1"
	s2 = Selection("y^2 < 2")
	assert s2.__repr__() == "y^2 < 2"
	assert s2.parsed.lhs.asList() == ['y', '^', '2']
	assert s2.parsed.operator == "<"
	assert s2.parsed.rhs == "2"
	s3 = s1 | s2
	assert s3.__repr__() == "x > 1 | y^2 < 2"
	s1 & s3
	assert s3.parsed[0].asList() == s1.parsed.asList()
	assert s3.parsed[1] == "|"
	assert s3.parsed[2].asList() == s2.parsed.asList()
	s4 = s1 & s2
	assert s4.__repr__() == "x > 1 & y^2 < 2"
	assert s4.parsed[1] == "&"
	s5 = Selection("z <= x")
	assert s5.__repr__() == "z <= x"
	assert s5.parsed.lhs == "z"
	assert s5.parsed.operator == "<="
	assert s5.parsed.rhs == "x"
	s6 = s4 | s5
	s6 = s5 | s4
	assert s6.__repr__() == "z <= x | (x > 1 & y^2 < 2)"
	s7 = s5 & s4
	assert s7.__repr__() == "z <= x & x > 1 & y^2 < 2"
	s8 = Selection("-x < 1")
	s9 = ( s4 | s5 ) & s6

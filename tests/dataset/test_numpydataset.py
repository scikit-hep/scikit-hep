#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.dataset.numpydataset module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest
import os

import numpy as np

from skhep.utils.provenance import ObjectOrigin  # these are not imported automatically
from skhep.dataset.numpydataset import *


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

ar = np.array([(1,1),(2,2),(3,3)],dtype=[('x',int), ('y',int)])

def test_constructors():
    ds = NumpyDataset(ar)

def test_properties():
    ds = NumpyDataset(ar, ObjectOrigin('simple_array'))
    assert type(ds.data) == np.ndarray
    assert ds.provenance.__repr__() == '<ObjectOrigin>'
    assert ds.mutable == True
    assert ds.immutable == False
    assert ds.transient == True
    assert ds.persistent == False

def test_methods():
    ds1 = NumpyDataset(ar)
    ds1.to_file('npds.npz')
    ds2 = NumpyDataset.from_file('npds.npz')
    assert ds2.provenance.__repr__() == '<FileOrigin (1 file)>'
    os.remove('npds.npz')

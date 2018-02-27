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
from skhep.dataset.selection import Selection


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

ar = np.array([(1,1),(2,2),(3,3)],dtype=[('x',int), ('y',int)])

def test_constructors():
    ds = NumpyDataset(ar)
    a = SkhepNumpyArray([1,2,3])

def test_properties():
    ds = NumpyDataset(ar, ObjectOrigin('simple_array'))
    assert type(ds.data) == np.ndarray
    assert ds.provenance[0].__repr__() == '<ObjectOrigin>'
    assert ds.mutable == True
    assert ds.immutable == False
    assert ds.transient == True
    assert ds.persistent == False
    with pytest.raises(NotImplementedError):
        ds.datashape

def test_methods():
    ds1 = NumpyDataset(ar)
    ds1.__repr__()
    assert ds1.__str__() == "[(1, 1) (2, 2) (3, 3)]"
    ds1.to_file('npds.npz')
    ds2 = NumpyDataset.from_file('npds.npz')
    assert ds2.provenance[0].__repr__() == '<FileOrigin (1 file)>'
    os.remove('npds.npz')
    with pytest.raises(IOError):
        ds = NumpyDataset.from_file('non_existent_file')
    ds3 = ds1.copy()
    assert ds1['x'].tolist() == [1,2,3]
    assert ds1.x.tolist() == [1,2,3]
    assert ds1.x.name == "x"
    assert ds1.x.provenance[0].detail == repr(ds1)
    ds1.z = np.ones((3,))
    assert ds1['z'].tolist() == [1,1,1]
    assert ds1.z.tolist() == [1,1,1]
    assert ds1.provenance[-1].__repr__() == "<Transformation(Array z has been created)>"
    ds1['w'] = np.zeros((3,))
    assert ds1.provenance[-1].__repr__() == "<Transformation(Array w has been created)>"
    assert ds1['w'].tolist() == [0,0,0]
    assert ds1.w.tolist() == [0,0,0]
    with pytest.raises(ValueError):
        ds1.__setitem__('h',np.ones((4,)))
    with pytest.raises(ValueError):
        ds1.__setitem__('k',"array")
    ds1.z = ds1.w
    assert ds1.provenance[-1].__repr__() =="<Transformation(Array z has been replaced by w)>"
    ds1.w = np.array([6,7,8])
    assert ds1.provenance[-1].__repr__() =="<Transformation(Array w has been replaced by array([6, 7, 8]))>"
    
def test_transformations():

    ds1 = NumpyDataset(ar)
    ds1.x += 1
    assert repr(ds1.provenance[-1]) == "<Transformation(1 has been added to x)>"
    ds1.x *= 2
    assert repr(ds1.provenance[-1]) == "<Transformation(x has been multiplied by 2)>"
    ds1.x -= 3
    assert repr(ds1.provenance[-1]) == "<Transformation(3 has been subtracted to x)>"
    ds1.x /= 4
    assert repr(ds1.provenance[-1]) == "<Transformation(x has been divided by 4)>"
    ds1.r = (ds1.x**2 + ds1.y**2)**0.5
    
def test_selections():
    ds1 = NumpyDataset(ar)
    sel = Selection("x > 1")
    ds2 = ds1.select(sel)
    ds2.provenance[-1] == "<Transformation(Selection, (x > 1), applied)>"
    assert ds2.__str__() == ds1.select("x > 1").__str__()
    ds3 = ds1[ds1.x > 1]
    assert repr(ds3.provenance[-1]) == "<Transformation(Subsetting dataset: x > 1)>"
    ds4 = ds1.select(ds1.x > 1)
    assert repr(ds4.provenance[-1]) == "<Transformation(Subsetting dataset: x > 1)>"
    ds5 = ds1.select("(x > 1) & (y > 1)")
    ds6 = ds1.select("min(x,y) > 1")
    ds7 = ds1.select("max(x,y) > 1")
    ds8 = ds1.select("( x * y ) > 1")
    with pytest.raises(ValueError):
        ds9 = ds1.copy()
        ds9.select(ds8.x)
#    dst = ds1.to_tree("DecayTree")
#    assert repr(dst.provenance[-1]) == "<Formatting to ROOTDataset(DecayTree)>"

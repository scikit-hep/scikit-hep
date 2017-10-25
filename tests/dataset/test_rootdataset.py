#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.dataset.rootdataset module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest

from random import gauss

# Obviously, skip all tests if the ROOT library is not available!
ROOT = pytest.importorskip('ROOT')

from ROOT import gROOT, TTree, AddressOf

from skhep.dataset.rootdataset import *

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

gROOT.ProcessLine(
"struct pyTTree {\
Int_t run;\
Int_t evt;\
Float_t x;\
Float_t y;\
Float_t z;\
}"
)
from ROOT import pyTTree
pytree = pyTTree()

def create_simple_tree():
    """Create a simple TTree with a couple of branches."""
    t = TTree('aTTree','A TTree')
    t.Branch('run', AddressOf(pytree, 'run'),'run/I')
    t.Branch('evt', AddressOf(pytree, 'evt'),'evt/I')
    t.Branch('x', AddressOf(pytree, 'x'),'x/F')
    t.Branch('y', AddressOf(pytree, 'y'),'y/F')
    t.Branch('z', AddressOf(pytree, 'z'),'z/F')
    for i in range(1000):
        pytree.run = 1 if (i<500) else 2
        pytree.evt = i
        pytree.x = gauss(0.,10.)
        pytree.y = gauss(0,10.)
        pytree.z = gauss(5.,50.)
        t.Fill()
    return t

tree = create_simple_tree()

def test_constructors():
    ds = ROOTDataset(tree)

def test_properties():
    pass

def test_methods():
    pass

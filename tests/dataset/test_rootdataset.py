#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.dataset.rootdataset module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest

import os
from random import gauss

# Obviously, skip all tests if the ROOT library is not available!
ROOT = pytest.importorskip('ROOT')

from ROOT import gROOT, TTree, TChain, TFile, AddressOf

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

def create_simple_tree(nevents):
    """Create a simple TTree with a couple of branches."""
    t = TTree('aTTree','A TTree')
    t.Branch('run', AddressOf(pytree, 'run'),'run/I')
    t.Branch('evt', AddressOf(pytree, 'evt'),'evt/I')
    t.Branch('x', AddressOf(pytree, 'x'),'x/F')
    t.Branch('y', AddressOf(pytree, 'y'),'y/F')
    t.Branch('z', AddressOf(pytree, 'z'),'z/F')
    for i in range(nevents):
        pytree.run = 1 if (i<500) else 2
        pytree.evt = i
        pytree.x = gauss(0., 10.)
        pytree.y = gauss(0, 10.)
        pytree.z = gauss(5., 50.)
        t.Fill()
    return t

def create_root_files():
    tree1 = create_simple_tree(200)
    tree2 = create_simple_tree(300)
    tname = tree1.GetName()
    f1 = TFile('tree1.root','create')
    tree1.Write()
    f1.Close()
    f2 = TFile('tree2.root','create')
    tree2.Write()
    f2.Close()
    fnames = ['tree1.root', 'tree2.root']
    del f1, f2
    del tree1, tree2
    return fnames, tname

tree = create_simple_tree(1000)
filenames, treename = create_root_files()
chain = TChain(treename)
for fn in filenames:
    chain.Add(fn)

def test_constructors():
    ds1 = ROOTDataset(tree)
    ds2 = ROOTDataset(chain)
    del ds1, ds2

def test_properties():
    ds1 = ROOTDataset(tree)
    assert ds1.provenance.__repr__() == '<ObjectOrigin>'
    assert ds1.mutable == True
    assert ds1.immutable == False
    assert ds1.transient == False
    assert ds1.persistent == True
    ds2 = ROOTDataset(chain)
    assert ds2.provenance.__repr__() == '<FileOrigin (2 files)>'
    del ds1, ds2

def test_methods():
    ds1 = ROOTDataset(tree)
    ds1.to_file('new_tree.root')
    assert os.path.isfile('new_tree.root') == True
    del ds1
    ds2 = ROOTDataset(chain)
    ds2.to_file('new_chain.root')
    assert os.path.isfile('new_chain.root') == True
    del ds2
    ds3 = ROOTDataset.from_file('new_tree.root', treename='aTTree')
    del ds3
    ds4 = ROOTDataset.from_file('new_tree.root')
    ds5 = ROOTDataset.from_file(['new_tree.root', 'new_chain.root'])
    ds6 = ROOTDataset.from_file('new*.root')
    del ds4, ds5, ds6
    os.remove('new_tree.root')
    os.remove('new_chain.root')

os.remove('tree1.root')
os.remove('tree2.root')

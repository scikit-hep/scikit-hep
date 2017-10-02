##!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from skhep.pdg import *
from skhep.utils.py23 import *
from pytest import approx

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
def test_pdt():
    tbl = ParticleDataTable('skhep/data/mass_width_2016.mcd')
    assert tbl('f(0)(500)0').name == tbl[9000221].name
    assert tbl('f(0)(500)0').id == 9000221
    assert tbl('nonexistentparticlename') == None
    #assert tbl.has_key(11)
    #assert tbl.has_particle(2212)
    assert tbl.particle(21).__repr__(),'g0: ID=21, m=0 GeV, 3*q=0 == width=0 GeV'

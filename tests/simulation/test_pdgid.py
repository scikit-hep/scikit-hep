#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.simulation.pdgid module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from skhep.simulation.pdgid import *
from skhep.utils.py23 import *
from pytest import approx


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
class PdgIdTest(object):
    def __init__(self):
        # Set of PDG IDs used for tests
        # FIXME: even better if IDs taken directly by name from the Particle Data Table
        # Bosons
        self.id_gluon = 21
        self.id_photon = 22
        self.id_Wminus = -24
        # Leptons
        self.id_nue = 12
        self.id_electron = 11
        # Light hadrons
        self.id_proton = 2212
        self.id_piminus = -211
        self.id_Kplus = 321
        self.id_Lambda = 3122
        self.id_Omegaminus = 3334
        # Charm hadrons
        self.id_Lcplus = 4122
        self.id_AntiOmegaccc = -4444
        # Beauty hadrons
        self.id_B0 = 511
        self.id_Bcminus = -541
        self.id_Lb = 5122
        # Di-quarks
        self.id_dd1 = 1103
        self.id_sd0 = 3101
        # Exotics
        self.id_gluino = 1000021
        # Invalid ID
        self.id_invalid1 = 0  # illegal ID
        self.id_invalid2 = 99999999  # general form is a 7-digit number

    def test_charge_functions(self):
        assert charge(self.id_gluon) == 0
        assert charge(self.id_photon) == 0
        assert charge(self.id_electron) == -1
        assert charge(self.id_proton) == +1
        assert charge(self.id_piminus) == -1
        assert charge(self.id_Kplus) == +1
        assert threeCharge(self.id_photon) == 0
        assert threeCharge(self.id_electron) == -3
        assert threeCharge(self.id_proton) == +3
        assert threeCharge(self.id_Kplus) == +3

    def test_spin_functions(self):
        assert jSpin(self.id_gluon) == 3
        assert jSpin(self.id_photon) == 3
        assert jSpin(self.id_electron) == 2
        assert jSpin(self.id_proton) == 2
        assert jSpin(self.id_piminus) == 1
        assert jSpin(self.id_Kplus) == 1
        #
        # assert  sSpin(self.id_photon   ) == 3
        # assert  sSpin(self.id_electron ) == 1
        # assert  sSpin(self.id_proton   ) == 1
        assert sSpin(self.id_piminus) == 0
        assert sSpin(self.id_Kplus) == 0
        #
        assert lSpin(self.id_photon) == None
        assert lSpin(self.id_electron) == None
        # assert  lSpin(self.id_proton   ) == None
        assert lSpin(self.id_piminus) == 0
        assert lSpin(self.id_Kplus) == 0

    def test_is_functions(self):
        assert isValid(self.id_gluon) == True
        assert isValid(self.id_photon) == True
        assert isValid(self.id_electron) == True
        assert isValid(self.id_proton) == True
        assert isValid(self.id_piminus) == True
        assert isValid(self.id_invalid1) == None
        assert isValid(self.id_invalid2) == False
        #
        assert isHadron(self.id_proton) == isBaryon(self.id_proton)
        assert isHadron(self.id_electron) == isBaryon(self.id_electron)
        #
        assert isHadron(self.id_gluon) == False
        assert isHadron(self.id_photon) == False
        assert isHadron(self.id_electron) == False
        assert isHadron(self.id_proton) == True
        assert isHadron(self.id_piminus) == True
        #
        assert isBaryon(self.id_gluon) == False
        assert isBaryon(self.id_photon) == False
        assert isBaryon(self.id_electron) == False
        assert isBaryon(self.id_proton) == True
        assert isBaryon(self.id_piminus) == False
        #
        assert isMeson(self.id_gluon) == False
        assert isMeson(self.id_photon) == False
        assert isMeson(self.id_electron) == False
        assert isMeson(self.id_proton) == False
        assert isMeson(self.id_piminus) == True
        #
        assert isLepton(self.id_gluon) == False
        assert isLepton(self.id_photon) == False
        assert isLepton(self.id_electron) == True
        assert isLepton(self.id_proton) == False
        assert isLepton(self.id_piminus) == False
        #
        assert isNucleus(self.id_gluon) == False
        assert isNucleus(self.id_photon) == False
        assert isNucleus(self.id_electron) == False
        assert isNucleus(self.id_proton) == True
        assert isNucleus(self.id_piminus) == False
        #
        assert isDiQuark(self.id_gluon) == False
        assert isDiQuark(self.id_photon) == False
        assert isDiQuark(self.id_electron) == False
        assert isDiQuark(self.id_proton) == False
        assert isDiQuark(self.id_piminus) == False
        #
        assert isDyon(self.id_gluon) == False
        assert isDyon(self.id_photon) == False
        assert isDyon(self.id_electron) == False
        assert isDyon(self.id_proton) == False
        assert isDyon(self.id_piminus) == False
        #
        assert isPentaquark(self.id_gluon) == False
        assert isPentaquark(self.id_photon) == False
        assert isPentaquark(self.id_electron) == False
        assert isPentaquark(self.id_proton) == False
        assert isPentaquark(self.id_piminus) == False
        # Other functions to test:
        # isQBall, isRhadron, isSUSY

    def test_has_functions(self):
        # assert  hasFundamentalAnti(self.id_photon  ) == False
        assert hasFundamentalAnti(self.id_electron) == True
        # assert  hasFundamentalAnti(self.id_proton  ) == True
        #
        assert hasUp(self.id_photon) == False
        assert hasUp(self.id_electron) == False
        assert hasUp(self.id_proton) == True
        assert hasUp(self.id_piminus) == True
        assert hasUp(self.id_Kplus) == True
        #
        assert hasDown(self.id_photon) == False
        assert hasDown(self.id_electron) == False
        assert hasDown(self.id_proton) == True
        assert hasDown(self.id_piminus) == True
        assert hasDown(self.id_Kplus) == False
        #
        assert hasStrange(self.id_photon) == False
        assert hasStrange(self.id_electron) == False
        assert hasStrange(self.id_proton) == False
        assert hasStrange(self.id_piminus) == False
        assert hasStrange(self.id_Kplus) == True
        #
        assert hasCharm(self.id_photon) == False
        assert hasCharm(self.id_electron) == False
        assert hasCharm(self.id_proton) == False
        assert hasCharm(self.id_piminus) == False
        assert hasCharm(self.id_Kplus) == False
        #
        assert hasBottom(self.id_photon) == False
        assert hasBottom(self.id_electron) == False
        assert hasBottom(self.id_proton) == False
        assert hasBottom(self.id_piminus) == False
        assert hasBottom(self.id_Kplus) == False
        #
        assert hasTop(self.id_photon) == False
        assert hasTop(self.id_electron) == False
        assert hasTop(self.id_proton) == False
        assert hasTop(self.id_piminus) == False
        assert hasTop(self.id_Kplus) == False

    def test_ion_functions(self):
        assert ionZ(self.id_electron) == None
        assert ionZ(self.id_proton) == 1
        #
        assert ionA(self.id_electron) == None
        assert ionA(self.id_proton) == 1
        #
        assert ionNlambda(self.id_electron) == None
        assert ionNlambda(self.id_proton) == 0

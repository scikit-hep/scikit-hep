#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.simulation.pdgid module.
"""


#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest
import pypdt

from skhep.simulation.pdgid import *
from skhep.utils.py23       import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        # Set of PDG IDs used for tests
 
        table = pypdt.ParticleDataTable()
        pdt = {}

        # Creates a dictionary mapping particle names to IDs within the range
        # used for the test

        for i in range(-4444, 1000022):
            if table[i] != None:
                pdt[table[i].name] = i

        # Bosons
        self.id_gluon  = pdt['g']
        self.id_photon = pdt['gamma']
        self.id_Wminus = pdt['W^-']

        # Leptons
        self.id_nue      = pdt['nu_e']
        self.id_electron = pdt['e^-']

        # Light hadrons
        self.id_proton     = pdt['p^+']
        self.id_piminus    = pdt['pi^-']
        self.id_Kplus      =  pdt['K^+']
        self.id_Lambda     = pdt['Lambda^0']
        self.id_Omegaminus = pdt['Omega^-']

        # Charm hadrons
        self.id_Lcplus       = pdt['Lambda_c^+']
        self.id_AntiOmegaccc = pdt['Omega*_ccc~^--']

        # Beauty hadrons
        self.id_B0      =  pdt['B^0']
        self.id_Bcminus =  pdt['B_c^-']
        self.id_Lb      =  pdt['Lambda_b^0']

        # Di-quarks
        self.id_dd1 = pdt['dd_1']
        self.id_sd0 = pdt['sd_0']

        # Exotics
        self.id_gluino = pdt['gluino']

        # Invalid ID
        self.id_invalid1 = 0        # illegal ID
        self.id_invalid2 = 99999999 # general form is a 7-digit number

    def runTest(self):
        # Required for Python 2.6 only
        self.test_charge_functions()
        self.test_spin_functions()
        self.test_is_functions()
        self.test_has_functions()
        self.test_ion_functions()

    def test_charge_functions(self):
        self.assertEqual( charge(self.id_gluon    ),  0 )
        self.assertEqual( charge(self.id_photon   ),  0 )
        self.assertEqual( charge(self.id_electron ), -1 )
        self.assertEqual( charge(self.id_proton   ), +1 )
        self.assertEqual( charge(self.id_piminus  ), -1 )
        self.assertEqual( charge(self.id_Kplus    ), +1 )
        self.assertEqual( threeCharge(self.id_photon   ),  0 )
        self.assertEqual( threeCharge(self.id_electron ), -3 )
        self.assertEqual( threeCharge(self.id_proton   ), +3 )
        self.assertEqual( threeCharge(self.id_Kplus    ), +3 )

    def test_spin_functions(self):
        self.assertEqual( jSpin(self.id_gluon    ), 3 )
        self.assertEqual( jSpin(self.id_photon   ), 3 )
        self.assertEqual( jSpin(self.id_electron ), 2 )
        self.assertEqual( jSpin(self.id_proton   ), 2 )
        self.assertEqual( jSpin(self.id_piminus  ), 1 )
        self.assertEqual( jSpin(self.id_Kplus    ), 1 )
        #
        #self.assertEqual( sSpin(self.id_photon   ), 3 )
        #self.assertEqual( sSpin(self.id_electron ), 1 )
        #self.assertEqual( sSpin(self.id_proton   ), 1 )
        self.assertEqual( sSpin(self.id_piminus  ), 0 )
        self.assertEqual( sSpin(self.id_Kplus    ), 0 )
        #
        self.assertEqual( lSpin(self.id_photon   ), None )
        self.assertEqual( lSpin(self.id_electron ), None )
        #self.assertEqual( lSpin(self.id_proton   ), None )
        self.assertEqual( lSpin(self.id_piminus  ), 0    )
        self.assertEqual( lSpin(self.id_Kplus    ), 0    )

    def test_is_functions(self):
        self.assertEqual( isValid(self.id_gluon    ), True  )
        self.assertEqual( isValid(self.id_photon   ), True  )
        self.assertEqual( isValid(self.id_electron ), True  )
        self.assertEqual( isValid(self.id_proton   ), True  )
        self.assertEqual( isValid(self.id_piminus  ), True  )
        self.assertEqual( isValid(self.id_invalid1 ), None  )
        self.assertEqual( isValid(self.id_invalid2 ), False )
        #
        self.assertEqual( isHadron(self.id_proton  ), isBaryon(self.id_proton  ) )
        self.assertEqual( isHadron(self.id_electron), isBaryon(self.id_electron) )
        #
        self.assertEqual( isHadron(self.id_gluon    ), False )
        self.assertEqual( isHadron(self.id_photon   ), False )
        self.assertEqual( isHadron(self.id_electron ), False )
        self.assertEqual( isHadron(self.id_proton   ), True  )
        self.assertEqual( isHadron(self.id_piminus  ), True  )
        #
        self.assertEqual( isBaryon(self.id_gluon    ), False )
        self.assertEqual( isBaryon(self.id_photon   ), False )
        self.assertEqual( isBaryon(self.id_electron ), False )
        self.assertEqual( isBaryon(self.id_proton   ), True  )
        self.assertEqual( isBaryon(self.id_piminus  ), False )
        #
        self.assertEqual( isMeson(self.id_gluon    ), False )
        self.assertEqual( isMeson(self.id_photon   ), False )
        self.assertEqual( isMeson(self.id_electron ), False )
        self.assertEqual( isMeson(self.id_proton   ), False )
        self.assertEqual( isMeson(self.id_piminus  ), True  )
        #
        self.assertEqual( isLepton(self.id_gluon    ), False )
        self.assertEqual( isLepton(self.id_photon   ), False )
        self.assertEqual( isLepton(self.id_electron ), True  )
        self.assertEqual( isLepton(self.id_proton   ), False )
        self.assertEqual( isLepton(self.id_piminus  ), False )
        #
        self.assertEqual( isNucleus(self.id_gluon    ), False )
        self.assertEqual( isNucleus(self.id_photon   ), False )
        self.assertEqual( isNucleus(self.id_electron ), False )
        self.assertEqual( isNucleus(self.id_proton   ), True  )
        self.assertEqual( isNucleus(self.id_piminus  ), False )
        #
        self.assertEqual( isDiQuark(self.id_gluon    ), False )
        self.assertEqual( isDiQuark(self.id_photon   ), False )
        self.assertEqual( isDiQuark(self.id_electron ), False )
        self.assertEqual( isDiQuark(self.id_proton   ), False )
        self.assertEqual( isDiQuark(self.id_piminus  ), False )
        #
        self.assertEqual( isDyon(self.id_gluon    ), False )
        self.assertEqual( isDyon(self.id_photon   ), False )
        self.assertEqual( isDyon(self.id_electron ), False )
        self.assertEqual( isDyon(self.id_proton   ), False )
        self.assertEqual( isDyon(self.id_piminus  ), False )
        #
        self.assertEqual( isPentaquark(self.id_gluon    ), False )
        self.assertEqual( isPentaquark(self.id_photon   ), False )
        self.assertEqual( isPentaquark(self.id_electron ), False )
        self.assertEqual( isPentaquark(self.id_proton   ), False )
        self.assertEqual( isPentaquark(self.id_piminus  ), False )
        # Other functions to test:
        # isQBall, isRhadron, isSUSY

    def test_has_functions(self):
        #self.assertEqual( hasFundamentalAnti(self.id_photon  ), False )
        self.assertEqual( hasFundamentalAnti(self.id_electron), True  )
        #self.assertEqual( hasFundamentalAnti(self.id_proton  ), True  )
        #
        self.assertEqual( hasUp(self.id_photon   ), False )
        self.assertEqual( hasUp(self.id_electron ), False )
        self.assertEqual( hasUp(self.id_proton   ), True  )
        self.assertEqual( hasUp(self.id_piminus  ), True  )
        self.assertEqual( hasUp(self.id_Kplus    ), True  )
        #
        self.assertEqual( hasDown(self.id_photon   ), False )
        self.assertEqual( hasDown(self.id_electron ), False )
        self.assertEqual( hasDown(self.id_proton   ), True  )
        self.assertEqual( hasDown(self.id_piminus  ), True  )
        self.assertEqual( hasDown(self.id_Kplus    ), False )
        #
        self.assertEqual( hasStrange(self.id_photon   ), False )
        self.assertEqual( hasStrange(self.id_electron ), False )
        self.assertEqual( hasStrange(self.id_proton   ), False )
        self.assertEqual( hasStrange(self.id_piminus  ), False )
        self.assertEqual( hasStrange(self.id_Kplus    ), True  )
        #
        self.assertEqual( hasCharm(self.id_photon   ), False )
        self.assertEqual( hasCharm(self.id_electron ), False )
        self.assertEqual( hasCharm(self.id_proton   ), False )
        self.assertEqual( hasCharm(self.id_piminus  ), False )
        self.assertEqual( hasCharm(self.id_Kplus    ), False )
        #
        self.assertEqual( hasBottom(self.id_photon   ), False )
        self.assertEqual( hasBottom(self.id_electron ), False )
        self.assertEqual( hasBottom(self.id_proton   ), False )
        self.assertEqual( hasBottom(self.id_piminus  ), False )
        self.assertEqual( hasBottom(self.id_Kplus    ), False )
        #
        self.assertEqual( hasTop(self.id_photon   ), False )
        self.assertEqual( hasTop(self.id_electron ), False )
        self.assertEqual( hasTop(self.id_proton   ), False )
        self.assertEqual( hasTop(self.id_piminus  ), False )
        self.assertEqual( hasTop(self.id_Kplus    ), False )

    def test_ion_functions(self):
        self.assertEqual( ionZ(self.id_electron ), None )
        self.assertEqual( ionZ(self.id_proton   ), 1    )
        #
        self.assertEqual( ionA(self.id_electron ), None )
        self.assertEqual( ionA(self.id_proton   ), 1    )
        #
        self.assertEqual( ionNlambda(self.id_electron ), None )
        self.assertEqual( ionNlambda(self.id_proton   ), 0    )

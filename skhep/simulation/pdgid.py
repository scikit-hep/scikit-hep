# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Module for PDG ID methods
=========================

Scikit-HEP simply wraps the functionality provided by the [PyPDT]_ package
to access in Python what is otherwise provided by the HepPID package in C++.
HepPID translates the standard PDG numbering scheme.

All methods from PyPDT applicable to the PDG particle identification codes,
a.k.a. PDG IDs, are available.

Functions available:

{0}

Standard use case:
    >>> from skhep.simulation import pdgid
    >>> pdgid.isLepton(11)
    True
    >>> pdgid.charge(-4444)  # anti Omega_ccc^++
    -2.0

**References**

.. [PyPDT] https://pypi.python.org/pypi/PyPDT.

"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from pypdt.pid import *

# Expose all functions imported from pypdt.pid
__all__ = ['isValid',
           'charge', 'threeCharge',
           'jSpin', 'lSpin', 'sSpin',
           'hasFundamentalAnti',
           'hasDown', 'hasUp', 'hasStrange', 'hasCharm', 'hasBottom', 'hasTop',
           'isLepton', 'isHadron', 'isBaryon', 'isMeson',
           'isNucleus', 'isDiQuark', 'isDyon', 'isPentaquark', 'isQBall', 'isRhadron', 'isSUSY',
           'ionA', 'ionNlambda', 'ionZ'
           ]

__doc__ = __doc__.format(__all__)

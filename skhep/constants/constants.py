# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Physical and other handy constants
==================================

All constants are computed in the HEP System of Units
as defined in the units module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from math import pi

from ..units import m, s, eplus, mole, joule

# -----------------------------------------------------------------------------
# Mathematical constants
# -----------------------------------------------------------------------------

two_pi = 2 * pi
half_pi = pi / 2
pi_sq = pi * pi

# -----------------------------------------------------------------------------
# Physical constants
# -----------------------------------------------------------------------------

# Speed of light in vacuum
c_light = 299792458 * m / s
c_light_sq = c_light * c_light

# Electron charge
eminus = - eplus  # electron charge
e_sq = eplus * eplus

# Avogadro constant (taken from CODATA)
Avogadro = 6.022140857e+23 / mole

# Planck constant (taken from CODATA)
h_Planck = 6.626070040e-34 * joule * s
hbar_Planck = h_Planck / two_pi
hbar = hbar_Planck
hbarc = hbar_Planck * c_light
hbarc_sq = hbarc * hbarc

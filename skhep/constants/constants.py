# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Physical and other handy constants
==================================

All constants are computed in the HEP System of Units
as defined in the units module.
"""

#-----------------------------------------------------------------------------
# Import statements
#----------------------------------------------------------------------------- 
from __future__ import absolute_import

from math import pi

from ..units import m, s

#-----------------------------------------------------------------------------
# Mathematical constants
#-----------------------------------------------------------------------------

twopi  = 2 * pi
halfpi = pi / 2
pi2    = pi * pi

#-----------------------------------------------------------------------------
# Physical constants
#-----------------------------------------------------------------------------

# Speed of light in vacuum
c_light   = 299792458 * m/s
c_squared = c_light * c_light

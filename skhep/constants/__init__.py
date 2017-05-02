# Licensed under a 3-clause BSD style license, see LICENSE.
"""
This package `skhep.constants` contains 2 sorts of constants:

  * Physical constants.
  * Common and/or handy constants.

All constants are computed in the HEP System of Units
as defined in the `skhep.units` package.

Typical use case::

    >>> from skhep.constants import c_light
    >>> from skhep.units     import picosecond, micrometer
    >>> tau_Bs = 1.5 * picosecond    # a particle lifetime, say the Bs meson's
    >>> ctau_Bs = c_light * tau_Bs   # ctau of the particle, ~450 microns
    >>> print ctau_Bs                # result in HEP units, so mm ;-)
    0.449688687
    >>> print ctau_Bs / micrometer   # result in micrometers
    449.688687

"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from .constants import *

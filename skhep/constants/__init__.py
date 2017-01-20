# Licensed under a 3-clause BSD style license, see LICENSE.
"""
************************
Subpackage for constants
************************

  * Physical constants.
  * Common/handy constants.

Typical use case::

>>> from skhep.constants import c_light
>>> from skhep.units     import picosecond, micrometer
>>> tau_Bs = 1.5 * picosecond    # a particle lifetime, say the Bs meson's
>>> ctau_Bs = c_light * tau_Bs   # ctau of the particle, roughly 450 microns
>>> print ctau_Bs   # result in HEP units, so mm ;-)
0.449688687
>>> print ctau_Bs / micrometer   # result in micrometers
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from .constants import *

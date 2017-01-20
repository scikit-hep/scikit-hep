# Licensed under a 3-clause BSD style license, see LICENSE.
"""
*************************************************************
Subpackage for physical units and commonly-used unit prefixes
*************************************************************

In HEP the standard set of basic units was originally defined by the CLHEP [1]_ project:

===================   ================== ====
Quantity              Name               Unit
===================   ================== ====
Length                millimeter         mm
Time                  nanosecond         ns
Energy                Mega electron Volt MeV
Positron charge       eplus
Temperature           kelvin             K
Amount of substance   mole               mol
Luminous intensity    candela            cd
Plane angle           radian             rad
Solid angle           steradian          sr
===================   ================== ====

It is largely based on the International System of units (SI) [2]_

   ===================   ========   ====
   Quantity              Name       Unit
   ===================   ========   ====
   Length                meter      m
   Time                  second     s
   Mass                  kilogram   kg
   Electric current      ampere     A
   Temperature           kelvin     K
   Amount of substance   mole       mol
   Luminous intensity    candela    cd
   ===================   ========   ====

but augments it with handy definitions as well as changing the basic length and time units.

Typical use case::

>>> from skhep.units import MeV
>>> massWindow = 100 * MeV  # define a 100 MeV mass window
----

**References**

.. [1] http://proj-clhep.web.cern.ch/proj-clhep/.
.. [2] http://www.physics.nist.gov/cuu/Units/index.html.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from .prefixes import *
from .units    import *

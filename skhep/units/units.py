# Licensed under a 3-clause BSD style license, see LICENSE.
"""
*************************
Module of HEP basic units
*************************

In HEP the standard set of basic units was originally defined by the CLHEP [1]_ project. It is:

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

----

**References**

.. [1] http://proj-clhep.web.cern.ch/proj-clhep/.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from math import pi

from .prefixes import *

# --------------------------------------------------------------------
# Units of length
# ---------------
millimeter  = 1.
millimeter2 = millimeter * millimeter
millimeter3 = millimeter * millimeter * millimeter

mm  = millimeter
mm2 = millimeter2
mm3 = millimeter3

meter  = kilo * millimeter
meter2 = meter * meter
meter3 = meter * meter * meter

m  = meter
m2 = meter2
m3 = meter3

centimeter  = centi * meter
centimeter2 = centimeter * centimeter
centimeter3 = centimeter * centimeter * centimeter

cm  = centimeter
cm2 = centimeter2
cm3 = centimeter3

kilometer = kilo * meter
kilometer2 = kilometer * kilometer
kilometer3 = kilometer * kilometer * kilometer

km  = kilometer
km2 = kilometer2
km3 = kilometer3

micrometer = micro * meter
micron     = micrometer
nanometer  = nano  * meter
angstrom   = 1e-10 * meter

femtometer = femto * meter
fermi      = femtometer

fm  = femtometer
fm2 = femtometer * femtometer
fm3 = femtometer * femtometer * femtometer

barn = 1.e-28 * meter2

millibarn = milli * barn
microbarn = micro * barn
nanobarn  = nano  * barn
picobarn  = pico  * barn
femtobarn = femto * barn
attobarn  = atto  * barn

mb = millibarn
nb = nanobarn
pb = picobarn
fb = femtobarn
ab = attobarn

invmb = 1. / millibarn
invnb = 1. / nanobarn
invpb = 1. / picobarn
invfb = 1. / femtobarn
invab = 1. / attobarn

# --------------------------------------------------------------------
# Units of time
# -------------
nanosecond  = 1.

second      = giga  * nanosecond
millisecond = milli * second
microsecond = micro * second
picosecond  = pico  * second
femtosecond = femto * second

ns = nanosecond
s  = second
ms = millisecond
ps = picosecond

minute = 60 * second
hour   = 60 * minute
day    = 24 * hour

hertz = 1. / second
kilohertz = kilo * hertz
megahertz = mega * hertz

Hz = hertz
kHz = kilo * hertz
MHz = mega * hertz
GHz = giga * hertz

# --------------------------------------------------------------------
# Units of energy
# ---------------
megaelectronvolt = 1.

electronvolt     = micro * megaelectronvolt
kiloelectronvolt = kilo  * electronvolt
gigaelectronvolt = giga  * electronvolt
teraelectronvolt = tera  * electronvolt
petaelectronvolt = peta  * electronvolt
exaelectronvolt  = exa   * electronvolt

eV  = electronvolt
keV = kiloelectronvolt
MeV = megaelectronvolt
GeV = gigaelectronvolt
TeV = teraelectronvolt
PeV = petaelectronvolt
EeV = exaelectronvolt

# --------------------------------------------------------------------
# Units of electric charge
# ------------------------
eplus = 1.    # positron charge

# --------------------------------------------------------------------
# Units of temperature
# --------------------
kelvin = 1.

# --------------------------------------------------------------------
# Units of amount of substance
# ----------------------------
mole = 1.

mol = mole

# --------------------------------------------------------------------
# Units of luminous intensity
# ---------------------------
candela = 1.

# --------------------------------------------------------------------
# Units of angles
# ---------------
radian      = 1.    # plane angle
milliradian = milli * radian

steradian   = 1.    # solid angle

degree = (pi/180.) * radian

rad  = radian
mrad = milliradian
sr   = steradian

deg  = degree

# --------------------------------------------------------------------
# Derived units
# -------------

# Electric potential [E][Q^-1]
megavolt = megaelectronvolt / eplus
volt     = micro * megavolt
kilovolt = kilo * volt

# --------------------------------------------------------------------
# Units derived from luminous intensity
# -------------------------------------

# Luminous flux [I]
lumen = candela * steradian

# Illuminance, i.e. amount of luminous flux per unit area [I][L^-2]
lux = lumen / meter2 

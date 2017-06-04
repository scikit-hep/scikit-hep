# Licensed under a 3-clause BSD style license, see LICENSE.
"""
*************************
Module of HEP basic units
*************************

In HEP the System of Units consists of the basic units originally defined by the [CLHEP]_ project:

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

It is largely based on the international system of units ([SI]_)

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

but augments it with handy definitions, changing the basic length and time units.

This module also defines an extensive set of derived units.

Typical use cases::

    >>> # add two quantities with length units and get the result im meters
    >>> from skhep import units as u
    >>> (1 * u.meter + 5 * u.cm) / u.meter
    1.05
    >>> from skhep.units import MeV, GeV
    >>> massWindow = 100 * MeV    # define a 100 MeV mass window
    >>> def energy_resolution():
    ...    # returns the energy resolution of 100 MeV
    ...    return 100 * MeV
    ...
    >>> energy_resolution() / GeV # get the energy resolution in GeV
    0.1

**References**

.. [CLHEP] http://proj-clhep.web.cern.ch/proj-clhep/.
.. [SI] http://www.physics.nist.gov/cuu/Units/index.html.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from math import pi

from .prefixes import *

# --------------------------------------------------------------------
# Units of length
# ---------------
millimeter = 1.
millimeter2 = millimeter * millimeter
millimeter3 = millimeter * millimeter * millimeter

mm = millimeter
mm2 = millimeter2
mm3 = millimeter3

meter = kilo * millimeter
meter2 = meter * meter
meter3 = meter * meter * meter

m = meter
m2 = meter2
m3 = meter3

centimeter = centi * meter
centimeter2 = centimeter * centimeter
centimeter3 = centimeter * centimeter * centimeter

cm = centimeter
cm2 = centimeter2
cm3 = centimeter3

kilometer = kilo * meter
kilometer2 = kilometer * kilometer
kilometer3 = kilometer * kilometer * kilometer

km = kilometer
km2 = kilometer2
km3 = kilometer3

micrometer = micro * meter
micron = micrometer
nanometer = nano * meter
angstrom = 1e-10 * meter

femtometer = femto * meter
fermi = femtometer

fm = femtometer
fm2 = femtometer * femtometer
fm3 = femtometer * femtometer * femtometer

barn = 1.e-28 * meter2

millibarn = milli * barn
microbarn = micro * barn
nanobarn = nano * barn
picobarn = pico * barn
femtobarn = femto * barn
attobarn = atto * barn

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
# --------------------------------------------------------------------
nanosecond = 1.

ns = nanosecond

second = giga * nanosecond
millisecond = milli * second
microsecond = micro * second
picosecond = pico * second
femtosecond = femto * second

s = second
ms = millisecond
ps = picosecond

minute = 60 * second
hour = 60 * minute
day = 24 * hour

hertz = 1. / second

kilohertz = kilo * hertz
megahertz = mega * hertz

Hz = hertz

GHz = giga * hertz
MHz = mega * hertz
kHz = kilo * hertz

# --------------------------------------------------------------------
# Units of energy
# --------------------------------------------------------------------
megaelectronvolt = 1.

electronvolt = micro * megaelectronvolt

exaelectronvolt = exa * electronvolt
petaelectronvolt = peta * electronvolt
teraelectronvolt = tera * electronvolt
gigaelectronvolt = giga * electronvolt
kiloelectronvolt = kilo * electronvolt

EeV = exaelectronvolt
PeV = petaelectronvolt
TeV = teraelectronvolt
GeV = gigaelectronvolt
MeV = megaelectronvolt
keV = kiloelectronvolt
eV = electronvolt

# --------------------------------------------------------------------
# Units of electric charge
# --------------------------------------------------------------------
eplus = 1.  # positron charge

# --------------------------------------------------------------------
# Units of temperature
# --------------------------------------------------------------------
kelvin = 1.

# --------------------------------------------------------------------
# Units of amount of substance
# --------------------------------------------------------------------
mole = 1.

mol = mole

# --------------------------------------------------------------------
# Units of luminous intensity
# --------------------------------------------------------------------
candela = 1.

cd = candela

# --------------------------------------------------------------------
# Units of angles
# --------------------------------------------------------------------
radian = 1.  # plane angle
steradian = 1.  # solid angle

rad = radian
sr = steradian

milliradian = milli * radian
mrad = milliradian

degree = (pi / 180.) * radian

deg = degree

# --------------------------------------------------------------------
# Derived units
# --------------------------------------------------------------------

# Positron charge [Coulomb]
e_SI = 1.6021766208e-19  # taken from CODATA

# Electric charge [Q]
# --------------------------------------------------------------------
coulomb = eplus / e_SI

# Electric current [Q][T^-1]
# -------------------------
ampere = coulomb / second

milliampere = milli * ampere
microampere = micro * ampere
nanoampere = nano * ampere

A = ampere

# Energy [E]
# ----------
joule = electronvolt / e_SI  # joule = 6.24150 e+12 * MeV

J = joule

# Power [M][L^2][T^-3]
watt = joule / second

W = watt

kW = kilo * watt
MW = mega * watt
GW = giga * watt

# Force [E][L^-1]
newton = joule / meter

N = newton

# Pressure
pascal = newton / meter2

Pa = pascal

bar = 1.e+5 * pascal

atmosphere = 101325 * pascal

# Mass [E][T^2][L^-2]
kilogram = joule * second * second / (meter * meter)
gram = milli * kilogram
milligram = milli * gram

kg = kilogram
g = gram
mg = milligram

# Electric potential
megavolt = megaelectronvolt / eplus
volt = micro * megavolt
kilovolt = kilo * volt

# Electric capacitance
farad = coulomb / volt

millifarad = milli * farad
microfarad = micro * farad
nanofarad = nano * farad
picofarad = pico * farad

# Electric resistance
ohm = volt / ampere

# Magnetic Field
tesla = volt * second / meter2

gauss = 1.e-4 * tesla

kilogauss = kilo * gauss

# Magnetic Flux
weber = volt * second  # weber = 1000*megavolt*ns

# Inductance
henry = weber / ampere

# --------------------------------------------------------------------
# Units derived from luminous intensity
# --------------------------------------------------------------------

# Luminous flux [I]
lumen = candela * steradian

# Illuminance, i.e. amount of luminous flux per unit area [I][L^-2]
lux = lumen / meter2

# --------------------------------------------------------------------
# Units for radiation
# --------------------------------------------------------------------

# Activity [T^-1]
becquerel = 1. / second

Bq = becquerel

curie = 3.7e+10 * becquerel

Ci = curie

# Absorbed dose [L^2][T^-2]
gray = joule / kilogram

Gy = gray

# Dose equivalent
sievert = joule / kilogram

Sv = sievert

# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Subpackage to handle Particle Data Tables
=========================================

Standard use case:
    >>> from skhep.pdg import ParticleDataTable
    >>> tbl = ParticleDataTable('data/mass_width_2016.mcd')   # doctest: +SKIP
    >>> tbl[9000221].name                                      # doctest: +SKIP
    f(0)(500)0                                                 # doctest: +SKIP
    >>> tbl('f(0)(500)0').id                                   # doctest: +SKIP
    9000221                                                    # doctest: +SKIP
    >>> tbl('f(0)(500)0').name                                 # doctest: +SKIP
    'f(0)(500)0'                                               # doctest: +SKIP

"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from pypdt.pdt import *


# Expose all classes imported from pdt
__all__ = [ 'ParticleData', 'ParticleDataTable', 'PDT' ]

#-----------------------------------------------------------------------------
# Extra functionality
#-----------------------------------------------------------------------------
def fromname(self,name):
    """Return the particle data given the PDG name. Returns None if not found."""
    for id in self.ids():
        if self[id].name == name: return self.get(id)
    return None

ParticleDataTable.__call__ = fromname

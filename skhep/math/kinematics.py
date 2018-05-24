# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Mathematical functions relevant to kinematics
=============================================
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from ..units import MeV, ns
from ..constants import hbar

from .numeric import isequal


def Kallen_function(x, y, z):
    """
    The Kallen function, aka triangle or lambda function,
    named after physicist Anders Olof Gunnar Kallen [Kallen]_.

    Definition
    ----------

    .. math::

      \\begin{eqnarray}
      \\lambda(x,y,z) &=& x^2 + y^2 + z^2 - 2 x y - 2 y z - 2 z x \\\\
                      &=& (x-y-z)^2 - 4 y z \\\\
                      &=& [ x - (\\sqrt{y}+\\sqrt{z})^2 ] [ x - (\\sqrt{y}-\\sqrt{z})^2 ] \\,\\,\\,\\mathrm{if} \\,\\,\\,y, z > 0
      \\end{eqnarray}

    Example
    -------
    Calculate in the rest frame of a particle of mass M decaying to 2 particles labeled 1 and 2,
    :math:`P (M) \\to p1 (m1) + p2 (m2)`, the momenta of 1 and 2 given by :math:`p = |\\mathbf{p1}| = |\\mathbf{p2}|`:

        >>> from skhep.math  import Kallen_function
        >>> from skhep.units import MeV, GeV
        >>> from math import sqrt
        >>> M = 5.279 * GeV; m1 = 493.7 * MeV; m2 = 139.6 * MeV
        >>> p = sqrt( Kallen_function( M**2, m1**2, m2**2 ) ) / (2*M)
        >>> print p / GeV   # print the CMS momentum in GeV
        2.61453580221

    References
    ----------
    .. [Kallen] https://en.wikipedia.org/wiki/K%C3%A4ll%C3%A9n_function
    """
    return (x - y - z) ** 2 - 4 * y * z  # faster to evaluate condensed form used

def Armenteros_Podolanski_variables(pplus_3Dvec, pminus_3Dvec):
    """
    Calculate the Armenteros Podolanski [APPaper]_ variables :math:`(\\alpha,q_T)` for a 2-body decay.

    Definition
    ----------

    .. math::

      \\alpha = \\frac{p_L^+ - p_L^-}{p_L^+ + p_L^-}

      q_T = \\frac{| p^- \\times p^{\\mathrm mother}|}{|p^{\\mathrm mother}|}

    where the longitudinal momentum along the direction of flight of the mother particle is

    .. math::

      p_L^\\pm = \\frac{p^\\pm \\cdot p^{\\mathrm mother}}{|p^{\\mathrm mother}|}

    and :math:`q_T` is the transverse momentum of the daughter particles with respect
    to the direction of flight of the mother particle.

    These expressions can be simplified to

    .. math::

      \\alpha = \\frac{|p^+|^2 - |p^-|^2}{|p^+ + p^-|^2}

      q_T = \\frac{| p^+ \\times p^- |}{|p^+ + p^-|}

    Parameters
    -----------
    pplus_3Dvec : Vector3D
        3D-momentum vector of the positively-charged daughter particle.
    pminus_3Dvec : Vector3D
        3D-momentum vector of the negatively-charged daughter particle.

    Returns
    -------
    Tuple :math:`(\\alpha,q_T)`.

    References
    ----------
    .. [APPaper] J. Podolanski and R. Armenteros, III. Analysis of V-events, The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science 45 (1954) 13, http://dx.doi.org/10.1080/14786440108520416
    """

    mother_mag = (pplus_3Dvec+pminus_3Dvec).mag
    if isequal (mother_mag, 0.0):
        raise ValueError( 'Total momentum has zero magnitude!')

    # Longitudinal momentum asymmetry, i.e. imbalance
    alpha = (pplus_3Dvec.mag2-pminus_3Dvec.mag2)/mother_mag**2

    # Transverse momentum of positively-charged particle along the mother particle momentum direction
    qT = (pplus_3Dvec.cross(pminus_3Dvec)).mag/mother_mag

    return (qT, alpha)


def lifetime_to_width(tau):
    """Convert from a particle lifetime to a decay width.

    Parameters
    -----------
    tau : float > 0
        Particle lifetime, typically in picoseconds (any HEP time unit is OK).

    Returns
    -------
    Particle decay width, in the HEP standard energy unit MeV.
    """

    if tau <= 0:
        raise ValueError( 'Input provided, %s <= 0!'.format(tau) )

    # Just need to first make sure that the lifetime is in the standard unit ns
    return hbar / float(tau / ns)


def width_to_lifetime(Gamma):
    """Convert from a particle decay width to a lifetime.

    Parameters
    ----------
    Gamma : float > 0
        Particle decay width, typically in MeV (any HEP energy unit is OK).

    Returns
    -------
    Particle lifetime, in the HEP standard time unit ns.
    """

    if Gamma <= 0.:
        raise ValueError( 'Input provided, %s <= 0!'.format(Gamma) )

    # Just need to first make sure that the width is in the standard unit MeV
    return hbar / float(Gamma / MeV)

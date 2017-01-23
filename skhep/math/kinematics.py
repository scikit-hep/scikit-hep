# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Mathematical functions relevant to kinematics
=============================================
"""

def Kallen_function( x, y, z ):
    """
    The Kallen, aka triangle or lambda function,
    named after physicist Anders Olof Gunnar Kallen.
    
    Definition
    ----------
    lambda(x,y,z) = x^2 + y^2 + z^2 -2*x*y - 2*y*z - 2*z*x
                  = (x-y-z)^2 - 4*y*z
                  = [ x - (sqrt(y)+sqrt(z))^2 ] * [ x - (sqrt(y)-sqrt(z))^2 ] if y, z > 0

    Example
    -------
    Calculate in the rest frame of a particle of mass M decaying to 2 particles labeled 1 and 2,
    P (M) -> p1 (m1) + p2 (m2), the momenta of 1 and 2 (p = |p1| = |p2|):
    >>> from skhep.math import Kallen_function
    >>> p = sqrt( Kallen_function( M**2, m1**2, m2**2 ) ) / (2*M)

    Reference
    ---------
    .. https://en.wikipedia.org/wiki/K%C3%A4ll%C3%A9n_function
    """
    return ( (x-y-z)**2 - 4*y*z )   # faster to evaluate condensed form used

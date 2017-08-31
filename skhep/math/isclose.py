#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# copied from https://raw.githubusercontent.com/PythonCHB/close_pep/master/is_close.py
# =============================================================================
"""
Test implementation for an isclose() function, for possible inclusion in
the Python standard library -- PEP0485

This version has multiple methods in it for experimentation and testing.

The ``final'' version can be found in isclose.py

This implementation is the result of much discussion on the python-ideas list
in January, 2015:

   https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031124.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031313.html

Copyright: Christopher H. Barker
License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php

"""
__all__ = (
    'isclose'       , ## close using relative and absolute distances 
    'distance_ulps' , ## distance in ULPs 
    'isclose_ulps'  , ## close in  terms of ULPs ?
    'isequal_ulps'  , ## isequal using  ULPs and SCALE
    'next_double'   , ## get next double 
    )

import cmath


def isclose(a,
            b,
            rel_tol=1e-9,
            abs_tol=0.0,
            method='weak'):
    """
    returns True if a is close in value to b. False otherwise

    :param a: one of the values to be tested

    :param b: the other value to be tested

    :param rel_tol=1e-8: The relative tolerance -- the amount of error
                         allowed, relative to the magnitude of the input
                         values.

    :param abs_tol=0.0: The minimum absolute tolerance level -- useful for
                        comparisons to zero.

    :param method: The method to use. options are:
                  "asymmetric" : the b value is used for scaling the tolerance
                  "strong" : The tolerance is scaled by the smaller of
                             the two values
                  "weak" : The tolerance is scaled by the larger of
                           the two values
                  "average" : The tolerance is scaled by the average of
                              the two values.

    NOTES:

    -inf, inf and NaN behave similar to the IEEE 754 standard. That
    -is, NaN is not close to anything, even itself. inf and -inf are
    -only close to themselves.

    Complex values are compared based on their absolute value.

    The function can be used with Decimal types, if the tolerance(s) are
    specified as Decimals::

      isclose(a, b, rel_tol=Decimal('1e-9'))

    See PEP-0485 for a detailed description

    """
    if method not in ("asymmetric", "strong", "weak", "average"):
        raise ValueError('method must be one of: "asymmetric",'
                         ' "strong", "weak", "average"')

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')

    if a == b:  # short-circuit exact equality
        return True
    # use cmath so it will work with complex or float
    if cmath.isinf(a) or cmath.isinf(b):
        # This includes the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite sign
        # would otherwise have an infinite relative tolerance.
        return False
    diff = abs(b - a)
    if method == "asymmetric":
        return (diff <= abs(rel_tol * b)) or (diff <= abs_tol)
    elif method == "strong":
        return (((diff <= abs(rel_tol * b)) and
                 (diff <= abs(rel_tol * a))) or
                (diff <= abs_tol))
    elif method == "weak":
        return (((diff <= abs(rel_tol * b)) or
                 (diff <= abs(rel_tol * a))) or
                (diff <= abs_tol))
    elif method == "average":
        return ((diff <= abs(rel_tol * (a + b) / 2) or
                (diff <= abs_tol)))
    else:
        raise ValueError('method must be one of:'
                         ' "asymmetric", "strong", "weak", "average"')

# =============================================================================
def distance_ulps ( a ,  b ) :
    """Distance in ULPS between two (floating point) numbers
    - it is assumed here that  size(long)==size(double) for underlying C-library
    :Example:
    >>> a = ...
    >>> b = ...
    >>> print distance_ulps ( a , b )
    """
    
    if   a == b : return 0
    elif a >  b : return -distance_ulps (  b ,  a )
    elif b <= 0 : return  distance_ulps ( -b , -a ) 
    elif a <  0 :
        return distance_ulps  ( 0 , -a ) + distance_ulps ( 0 , b )

    ## here a and b has same sign
    import ctypes

    a , b =  abs ( a ) , abs ( b )
    
    aa = ctypes.c_double ( float ( a ) ) 
    bb = ctypes.c_double ( float ( b ) ) 

    al = ctypes.c_long.from_buffer ( aa ).value
    bl = ctypes.c_long.from_buffer ( bb ).value 

    return bl - al 

# =============================================================================
def next_double ( a , ulps = 1 ) :
    """ Get the ``next-double'' by certaint ULPs distance
    :Example:
    >>> a = next_double ( 1 , 1 )
    >>> print a , a - sys.float_info.epsilon
    """
    
    a = float ( a ) 
    if 0 == ulps : return  a  
    if a < 0     : return -next_double ( -a , -ulps )

    if 0 > ulps  :
        d =  distance_ulps ( a , 0.0 ) + ulps
        if d < 0 : return -next_double ( 0.0 , -d )
        
    import ctypes
    
    aa  = ctypes.c_double ( a         ) 
    al  = ctypes.c_long.from_buffer   ( aa ).value
    al  = ctypes.c_long   ( al + ulps ) 
    aa  = ctypes.c_double.from_buffer ( al ).value
    
    return aa  
    

# =============================================================================
def isclose_ulps ( a  , b , ulps = 1000 ) :
    """Are two floating point numbers close enough (in units is ULPs)?
    :Example:
    >>> a = ...
    >>> b = ...
    >>> print isclose_ulps ( a , b , 1000 )
    """
    return ( a == b ) or ulps >= abs ( distance_ulps ( a ,  b ) ) 

# =============================================================================
def isequal ( a , b , scale = 1.0 , ulps = 1000 ) :
    """Are  two numbers ``a'' and ``b''  close enough ?
    Numbers are considere to be  equal is :
    - they are close enough in ULPS
    OR for scale != 0 
    - the difference is small enough compared to the specified scale,
    namely if ( scale + a - b == scale)
    
    :Example:
    >>> a =  sys.float_info.epsilon
    >>> b = -sys.float_info.epsilon
    
    """
    return ( a ==  b )  or isclose_ulps ( a , b , ulps ) or ( scale and isclose_ulps ( ( a - b ) + scale , scale , ulps ) ) 
    
# =============================================================================
## The END
# =============================================================================

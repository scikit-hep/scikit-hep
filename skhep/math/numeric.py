#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Licensed under a 3-clause BSD style license, see LICENSE.
# =============================================================================
""" Set of utilities for coparison of  floating point numbers inpired by
- https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
and the previous version:
- http://www.cygnus-software.com/papers/comparingfloats/Obsolete%20comparing%20floating%20point%20numbers.htm
"""
# =============================================================================
__all__ = (
    'distance_ulps' , ## distance in ULPs 
    'isclose_ulps'  , ## close in  terms of ULPs ?
    'isequal_ulps'  , ## isequal using  ULPs and SCALE
    'next_double'   , ## get next double 
    )
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
    """ Get the ``next-double'' by certain ULPs distance
    
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
def isequal ( a , b , scale = 1.0 , absdiff = 0.0 , ulps = 1000 ) :
    """Are  two numbers ``a'' and ``b''  close enough ?
    Numbers are considere to be  equal is :
    - they are close enough in ULPS
    - OR, for absdiff >0 , the absolute difference is smaller than absdiff
    - OR, for scale != 0 , the difference is small enough compared to the specified scale,
    
    :Example:
    >>> isequal(1,1+sys.float_info.epsilon)      
    True
    >>> isequal(1,1+sys.float_info.epsilon, ulps = 0 )
    False
    >>> isequal(1,1+sys.float_info.epsilon, scale = 100 , ulps = 0 )
    True
    """
    return ( a ==  b )  or ( 0 < absdiff and abs ( a - b ) < absdiff ) or isclose_ulps ( a , b , ulps ) or ( scale and isclose_ulps ( ( a - b ) + scale , scale , ulps ) ) 
    
# =============================================================================
## The END
# =============================================================================

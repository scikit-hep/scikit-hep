#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.math.geometry module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from skhep.math.geometry import *
from skhep.utils.py23 import *

import pytest
from pytest import approx

from math import pi

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
def test_geometry_constructors():
    
    v1  = Vector3D ( )
    p1  = Point3D  ( )
    assert str(p1)  == "Point3D(x=0.0,y=0.0,z=0.0)"
    assert repr(p1) == "<Point3D(x=0.0,y=0.0,z=0.0)>"
    
    l1  = Line3D   ( p1 , Vector3D ( 0 , 0 , 1 ) )
    assert str(l1)  == "Line3D({0},{1})"   .format(p1, Vector3D ( 0 , 0 , 1 ))
    assert repr(l1) == "<Line3D({0},{1})>" .format(p1, Vector3D ( 0 , 0 , 1 ))
    
    pl1 = Plane3D  ( p1 , Vector3D ( 0 , 0 , 1 ) )
    assert str(pl1)  == "Plane3D({0},{1})"   .format(p1, Vector3D ( 0 , 0 , 1 ))
    assert repr(pl1) == "<Plane3D({0},{1})>" .format(p1, Vector3D ( 0 , 0 , 1 ))

    l2  = Line3D  .from_points         ( p1 , Point3D(1,2,3) )
    pl2 = Plane3D .from_points         ( p1 , Point3D(1,2,3) , Point3D (3,2,1) )
    p2  = Point3D .frompoint           ( 1, 1, 1 )
    pl3 = Plane3D .from_line_and_point ( l1 , p2 )
    
    
    p3 = Point3D.fromiterable([1., 1., 1.])
    assert p3 == Point3D(1., 1., 1.)
    p4 = Point3D.fromcylindricalcoords(1., 0., 1.)
    assert p4 == Point3D(1., 0., 1.)
    assert p4.rho   == 1.
    p5 = Point3D.fromsphericalcoords(1.0, 0., 0.)
    assert p5 == Point3D(0., 0., 1.)
    assert p5.theta == 0.
    assert p5.phi   == 0.
    
    v2  = Vector3D ( 1, 1, 1)
    with pytest.raises(NotImplementedError):
        Line3D.__init__(Line3D(), p1, p1)
    with pytest.raises(NotImplementedError):
        Line3D.__init__(Line3D(), v2, v2)
    with pytest.raises(ValueError):
        Line3D.__init__(Line3D(), p1, v1)
        
    with pytest.raises(NotImplementedError):
        Plane3D.__init__(Plane3D(), p1, p1)
    with pytest.raises(NotImplementedError):
        Plane3D.__init__(Plane3D(), v2, v2)
    with pytest.raises(ValueError):
        Plane3D.__init__(Plane3D(), p1, v1)

def test_operators ():
    v1 = Vector3D(1,2,3)
    v2 = Vector3D(3,2,1)
    p1 = Point3D (0,0,1)
    p2 = Point3D (0,1,0)
    line1 = Line3D( p1 , v1)
    line2 = Line3D( p2 , v2)
    plane1 = Plane3D( p1 , v1)
    plane2 = Plane3D( p2 , v2)
    
    assert p1 + v1 == Point3D (1,2,4)
    assert v1 + p1 == Point3D (1,2,4)
    
    assert p1 - v1 == Point3D (-1,-2,-2)
    assert p1 - p2 == Vector3D(0,-1,1)
    
    p1 -= v1
    p1 += v1
    
    assert p1 == p1
    assert p1 != p2
    
    assert line1 == line1
    assert line1 != line2
    
    assert plane1 == plane1
    assert plane1 != line2


def test_contains():
    line  = Line3D   ( Point3D() , Vector3D(0,0,1) )
    plane = Plane3D  ( Point3D() , Vector3D(0,0,1) )

    assert Point3D(0,0,-10) in line
    assert Point3D(1,0,-10) not in line

    assert Point3D(1,0,0) in plane
    assert Point3D(0,1,0) in plane
    assert Point3D(0,0,2) not in plane

    linex = Line3D(  Point3D() , Vector3D(1,0,0) )
    liney = Line3D(  Point3D() , Vector3D(0,1,0) )
    linez = Line3D(  Point3D() , Vector3D(0,0,1) )

    assert linex in plane
    assert liney in plane
    assert linez not in plane


def test_distance():
    
    with pytest.raises(NotImplementedError):
        Point3D.distance(Point3D(), 2.)
    with pytest.raises(NotImplementedError):
        Line3D.distance(Line3D(), 2.)
    with pytest.raises(NotImplementedError):
        Plane3D.distance(Plane3D(), 2.)
    
    p0 = Point3D()
    p1 = Point3D(1,0,0)

    assert p0.distance(p0) == 0
    assert p0.distance(p1) == 1

    line = Line3D( Point3D() , Vector3D(0,0,1) )

    assert p0.distance(line) == 0
    assert p1.distance(line) == 1

    assert line.distance(p0) == 0
    assert line.distance(p1) == 1

    plane = Plane3D  ( Point3D(1,1,0) ,  Vector3D(0,0,1) )

    assert plane.distance(plane) == 0
    assert plane.distance(p0) == 0

    line1 = Line3D ( Point3D(1,2,3) , Vector3D (4,5,6) )
    line2 = Line3D ( Point3D(0,0,1) , Vector3D (1,1,0) )

    assert plane.distance(line1) == 0
    assert plane.distance(line2) == 1
    assert line1.distance(plane) == 0
    assert line2.distance(plane) == 1
    
    line3 = Line3D ( Point3D(0,0,2) , Vector3D (1,1,0) )
    
    assert line3.distance(line2) == 1
    
def test_angle():
    
    p0 = Point3D()
    
    with pytest.raises(NotImplementedError):
        Line3D.angle(Line3D(), p0)
    with pytest.raises(NotImplementedError):
        Plane3D.angle(Plane3D(), p0)
    
    line0  = Line3D   ( Point3D() , Vector3D(0,0,1) )
    line1  = Line3D   ( Point3D(0,0,1) , Vector3D(0,1,0) )

    plane0 = Plane3D  ( Point3D() , Vector3D(0,0,1) )
    plane1 = Plane3D  ( Point3D(0,0,1) , Vector3D(0,1,0) )
    
    assert line0.angle ( line1 ) == pi/2.
    assert line1.angle ( line0 ) == pi/2.
    assert line1.angle ( line1 ) == 0.
    assert line0.angle ( plane0 ) == 0.
    assert line0.angle ( plane1 ) == pi/2.
    assert line1.angle ( plane0 ) == pi/2.
    assert line1.angle ( plane1 ) == 0.
    
    assert plane0.angle ( plane1 ) == pi/2.
    assert plane1.angle ( plane0 ) == pi/2.
    assert plane1.angle ( plane1 ) == 0.
    
    assert plane0.angle ( line0 ) == 0.
    assert plane0.angle ( line1 ) == pi/2.
    assert plane1.angle ( line0 ) == pi/2.
    assert plane1.angle ( line1 ) == 0.

    
def test_intersect():

    with pytest.raises(NotImplementedError):
        Line3D.intersect(Line3D(), 1)
    with pytest.raises(NotImplementedError):
        Plane3D.intersect(Plane3D(), 1)
    
    p0 = Point3D()
    p1 = Point3D(0,0,1)
    
    line0  = Line3D   ( Point3D() , Vector3D(0,0,1) )
    line1  = Line3D   ( Point3D(0,0,1) , Vector3D(0,1,0) )

    plane0 = Plane3D  ( Point3D() , Vector3D(0,0,1) )
    plane1 = Plane3D  ( Point3D(0,0,1) , Vector3D(0,1,0) )
    
    assert line0.intersect( p0 ) == p0
    assert line0.intersect( p1 ) == p1
    assert line1.intersect( p0 ) == None
    assert line1.intersect( p1 ) == p1
    
    assert line0.intersect( line1 ) == Point3D(0,0,1)
    assert line1.intersect( line0 ) == Point3D(0,0,1)
    
    assert line0.intersect( plane0 ) == Point3D()
    assert line0.intersect( plane1 ) == line0
    assert line1.intersect( plane0 ) == None
    assert line1.intersect( plane1 ) == Point3D(0,0,1)
        
    assert plane0.intersect( p0 ) == p0
    assert plane0.intersect( p1 ) == None
    assert plane1.intersect( p0 ) == p0
    assert plane1.intersect( p1 ) == p1
    
    assert plane0.intersect( line0 ) == Point3D()
    assert plane0.intersect( line1 ) == None
    assert plane1.intersect( line0 ) == line0
    assert plane1.intersect( line1 ) == Point3D(0,0,1)
    
    assert plane0.intersect( plane1 ) == Line3D( Point3D() , Vector3D(1,0,0) )
    assert plane1.intersect( plane0 ) == Line3D( Point3D() , Vector3D(1,0,0) )
    
    assert plane0.intersect( plane0 ) == None
    line2  = Line3D   ( Point3D(0,1,0) , Vector3D(0,0,1) )
    assert line2.intersect( line0 ) == None
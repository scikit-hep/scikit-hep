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

from pytest import approx

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
def test_geometry_constructors():
    v1  = Vector3D ( )
    assert str(v1) == str((0., 0., 0.))
    p1  = Point3D  ( )
    l1  = Line3D   ( p1 , Vector3D ( 0 , 0 , 1 ) )
    pl1 = Plane3D  ( p1 , Vector3D ( 0 , 0 , 1 ) )

    l2  = Line3D .from_points ( p1 , Point3D(1,2,3) )
    pl2 = Plane3D.from_points ( p1 , Point3D(1,2,3) , Point3D (3,2,1) )

def test_operators ():
    v1 = Vector3D(1,2,3)
    v2 = Vector3D(3,2,1)
    p1 = Point3D (0,0,1)
    p2 = Point3D (0,1,0)

    v1 + v2
    v1 - v2

    p1 + v1
    v1 + p1

    p1 - v1
    p1 - p2

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


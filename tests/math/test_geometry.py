#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.math.geometry module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import unittest

from skhep.math.geometry import *
from skhep.utils.py23 import *

# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_geometry_constructors()
        self.test_operators  ()
        self.test_contains   ()
        self.test_distance   ()
        
    def test_geometry_constructors(self):
        
        v1  = Vector3D ( )
        self.assertEqual(str(v1), str((0., 0., 0.)))
        p1  = Point3D  ( )
        l1  = Line3D   ( p1 , Vector3D ( 0 , 0 , 1 ) )
        pl1 = Plane3D  ( p1 , Vector3D ( 0 , 0 , 1 ) )

        l2  = Line3D .from_points ( p1 , Point3D(1,2,3) )
        pl2 = Plane3D.from_points ( p1 , Point3D(1,2,3) , Point3D (3,2,1) )
        
    def test_operators (self):
        
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

    def test_contains ( self ) :

        line  = Line3D   ( Point3D() , Vector3D(0,0,1) ) 
        plane = Plane3D  ( Point3D() , Vector3D(0,0,1) )
        
        self.assertTrue  ( Point3D(0,0,-10) in line , 'Point must be in line!')
        self.assertFalse ( Point3D(1,0,-10) in line , 'Point must not be in line!')
        
        self.assertTrue  ( Point3D(1,0,0) in plane , 'Point must be in plane!')
        self.assertTrue  ( Point3D(0,1,0) in plane , 'Point must be in plane!')
        self.assertFalse ( Point3D(0,0,2) in plane , 'Point must not be in line!')

        linex = Line3D(  Point3D() , Vector3D(1,0,0) )
        liney = Line3D(  Point3D() , Vector3D(0,1,0) )
        linez = Line3D(  Point3D() , Vector3D(0,0,1) )
        
        self.assertTrue  ( linex in plane  , 'Line must be in plane!' )
        self.assertTrue  ( liney in plane  , 'Line must be in plane!' )
        self.assertFalse ( linez in plane  , 'Line must not be in plane!' )


    def test_distance ( self ) :

        p0 = Point3D()
        p1 = Point3D(1,0,0)
        
        self.assertEqual ( p0.distance(p0)  , 0 , 'Point-Point distance must be 0') 
        self.assertEqual ( p0.distance(p1)  , 1 , 'Point-Point distance must be 1') 
        
        line = Line3D( Point3D() , Vector3D(0,0,1) )
        
        self.assertEqual ( p0.distance(line) , 0 , 'Point-Line distance must be 0') 
        self.assertEqual ( p1.distance(line) , 1 , 'Point-Line distance must be 1') 
        
        self.assertEqual ( line.distance(p0) , 0 , 'Line-Point distance must be 0') 
        self.assertEqual ( line.distance(p1) , 1 , 'Line-Point distance must be 1') 
        
        plane = Plane3D ( Point3D(1,1,0) ,  Vector3D(0,0,1) )
        
        
        
Test().runTest()

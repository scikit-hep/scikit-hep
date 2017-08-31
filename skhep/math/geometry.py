#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Licensed under a 3-clause BSD style license, see LICENSE.
# =============================================================================
"""
Geometry classes
================

Three geometry classes are available:
* ``Point3D``      : a point in 3-dimensional space 
* ``Line3D``       : a line  in 3-dimensional space 
* ``Plane3D``      : a plane in 3-dimensional space 

"""
# =============================================================================
__all__  = (
    'Vector3D' , ## 3D-vector 
    'Point3D'  , ## 3D-point 
    'Line3D'   , ## line in 3D 
    'Plane3D'  , ## plane in 3D 
    )
# =============================================================================
# Import statements
# =============================================================================
from   skhep.math.vectors import Vector3D


# =============================================================================
# 3D-point
# =============================================================================
class Point3D(object) :
    """Point in 3D space 
    """
    def __init__ ( self , *args , **kwargs ) :
        self._vct = Vector3D( *args , **kwargs )
        
    @classmethod
    def origin(cls):
        """Shortcut constuctor for the origin (x=0.,y=0.,z=0.).
        Equivalent to the default constructor Point3D().
        """
        return cls(0., 0., 0.)

    @classmethod
    def frompoint(cls, x, y, z):
        """Constructor from an explicit space point."""
        return cls(x, y, z)

    @classmethod
    def fromvector(cls, other):
        """Copy constructor."""
        return cls(other.x, other.y, other.z)

    @classmethod
    def fromsphericalcoords(cls, r, theta, phi):
        """Constructor from a space point specified in spherical coordinates.

        r     : radius, the radial distance from the origin (r > 0)
        theta : inclination in radians (theta in [0, pi] rad)
        phi   : azimuthal angle in radians (phi in [0, 2pi) rad)
        """
        from math import sin, cos 
        x = r * sin(theta) * cos(phi)
        y = r * sin(theta) * sin(phi)
        z = r * cos(theta)
        return cls(x, y, z)

    @classmethod
    def fromcylindricalcoords(cls, rho, phi, z):
        """Constructor from a space point specified in cylindrical coordinates.

        rho : radial distance from the z-axis (rho > 0)
        phi : azimuthal angle in radians (phi in [-pi, pi) rad)
        z   : height
        """
        from math import sin, cos 
        x = rho * cos(phi)
        y = rho * sin(phi)
        z = z
        return cls(x, y, z)

    @classmethod
    def fromiterable(cls, values):
        """Constructor from a suitable iterable object.
        Suitable means here that all entries are numbers
        and the length equals 3.
        """
        values = list(values)
        if not len(values)==3:
            raise ValueError( 'Input iterable length = {0}! Please check your inputs.'.format(len(values)) )
        for i, v in enumerate(values):
            if not isinstance( v, (int,float) ):
                raise ValueError( 'Component #{0} is not a number!'.format(i) )
        return cls(values[0], values[1], values[2])

    
    @property
    def x(self):
        """Return the x, aka first coordinate at position 0."""
        return self._vct.x

    @x.setter
    def x(self, value):
        """Sets x, aka first coordinate at position 0."""
        self._vct.x = value

    @property
    def y(self):
        """Return the y, aka second coordinate at position 1."""
        return self._vct.y 

    @y.setter
    def y(self, value):
        """Sets y, aka second coordinate at position 1."""
        self._vct.y = value 

    @property
    def z(self):
        """Return the z, aka third coordinate at position 2."""
        return self._vct.z 

    @z.setter
    def z(self, value):
        """Sets z, aka third coordinate at position 2."""
        self._vct.z = value
        
    @property
    def rho(self):
        """Return the cylindrical coordinate rho."""
        return self._vct.rho 

    @property
    def theta(self, deg=False):
        """Return the spherical coordinate theta.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        raise self._vct.theta 

    @property
    def phi(self, deg=False):
        """Return the spherical or cylindrical coordinate phi.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        raise self._vct.phi 

    def __setitem__(self, i, value) :
       """Update/set the ith points component (commencing at 0, of course)."""
       self._vct[i] = value

    def __getitem__(self, i):
        """Get the ith point component (commencing at 0, of course)."""
        return self._vct[i]
    
    def tolist(self):
        """Return the vector as a list."""
        return self._vct.tolist() 
    
    def __len__(self):
        """Length/dimension of the poit, i.e. the number of elements = 3."""
        return 3 

    @property
    def mag(self):
        """Magnitude, a.k.a. norm, of the point."""
        return self._vct.mag 

    @property
    def mag2(self):
        """Square of the magnitude, a.k.a. norm, of the point."""
        return self._vct.mag2

    def __eq__  ( self , another ) :
        """Equality of two points
        :Example:
        >>> p1 = ...
        >>> p2 = ...
        >>> print  p1 == p2
        """
        return self._vct ==  another._vct
    
    def __ne__  ( self , another ) :
        """Non-equality of two points
        :Example:
        >>> p1 = ...
        >>> p2 = ...
        >>> print  p1 != p2
        """
        return self._vct !=  another._vct
    
    ## operations
    def __iadd__ ( self , vector ) :
        """Add vector to point
        
        :Example:
        
        >>> p  = Point3D  ( ... )
        >>> v  = Vector3D ( ... )
        >>> p += v  
        """
        
        if isinstance ( vector , Vector3D ) :
            self._vct += vector
            return self
        return NotImplemented
    
    def __isub__ ( self , vector ) :
        """Subtract vector from point
        
        :Example:
        
        >>> p  = Point3D  ( ... )
        >>> v  = Vector3D ( ... )
        >>> p -= v  
        """
        
        if isinstance ( vector , Vector3D ) :
            self._vct -= vector
            return self
        return NotImplemented 

    ## operations
    def __add__ ( self , vector ) :
        """ Addition of point and vector
        
        point + vector  --> point 
        
        """
        ## point + vector = point
        if isinstance ( vector , Vector3D ) :
            newpoint  = Point3D.fromvector ( self._vct )
            newpoint += vector
            return newpoint
        
        return NotImplemented 

    def __sub__ (  self , other ) :
        """ Subtraction for points and vectors
        1. point - point   -->  vector
        2. point - vector  -->  point
        
        """
        ## point - point  --> vector
        if isinstance ( other , Point3D ) : return self._vct - other._vct
        
        ## point - vector --> point 
        if isinstance ( other , Vector3D ) :
            newpoint  = Point3D.fromvector ( self._vct )
            newpoint -= other
            return newpoint

        return NotImplemented 

    def __radd__ ( self , other )  :
        """Right addition of vector and point"""
        return other + self

    def __repr__(self):
        """Class representation."""
        return "<Point3D (x={0},y={1},z={2})>".format(self.x,self.y,self.z)

    def __str__(self):
        """Simple class representation."""
        return "Point3D(x={0},y={1},z={2})".format(self.x,self.y,self.z)

    #
    def on_line  ( self , line ) :
        """In the point on the line?
        """
        v = line.point - self
        return 0 == v.mag2 or line.iscollinear  ( v ) 
    
    def on_plane ( self , plane ) :
        """In the point on the plane?
        """
        v = plane.point - self
        return 0 == v.mag2 or plane.normal.isperpendicular ( v ) 
        

# =============================================================================
# 3D-Line
# =============================================================================
class Line3D(object) :
    """Line in 3D space
    """
    def __init__ ( self                            ,
                   point  = Point3D  ( 0  ,0 , 0 ) ,
                   vector = Vector3D ( 0 , 0 , 1 ) ) :
        
        if not isinstance ( point  ,  Point3D  ) :
            raise NotImplementedError("Line3D: invalid ``point'' argument" )
        if not isinstance ( vector ,  Vector3D ) :
            raise NotImplementedError("Line3D: invalid ``vector'' argument" )
        
        if 0 == vector.mag2  :
            raise ValueError ("Line3D: ``vector'' must be zero!" )
            
        self.point  = Point3D .fromvector ( point  ) 
        self.vector = Vector3D.fromvector ( vector )  

    @classmethod
    def from_points ( cls , point1 , point2 ) :
        """Create the line from two points
        
        point1 : the first point on the line
        point2 : the second point on the line

        """
        return cls ( point1 , point2 - point1 ) 
    
    @classmethod
    def from_line   ( cls , line  ) :
        """Create the line from anoother line 
        """
        return cls ( line.point , line.vector ) 
    
    def __repr__(self):
        """Simple class representation."""

    def __repr__(self):
        """Simple class representation."""
        return "<Line3D({0},{1})>".format( self.point , self.vector ) 

    def __str__(self):
        """Simple class representation."""
        return "Line3D({0},{1})".format( self.point , self.vector ) 

    ## is the point on line ? 
    def __contains__ ( self , point ) :
        """Is the point on the line ?
        
        :Example:
        >>> line  = ...
        >>> point = ...
        >>> if point in line : ...
        """
        return point.on_line ( self )

    def iscollinear ( self , other ) :
        """Is the line collinear to another line or vector?
        """
        if   isinstance ( other , Line3D   ) : other = other.vector 
        elif isinstance ( other , Vector3D ) : pass
        else : raise TypeError("Line3D.iscollinear: invalid ``other'' argument" )
        ##
        return self.vector.iscollinear ( other  )

    def on_plane ( self , plane ) :
        """In the line on the plane?
        """
        return self.point.on_plane ( plane ) and self.vector.isperpendicular ( plane.normal )

    def point_on_line (  self , mu ) :
        """ Get the point on line, that  corresponds to parameter ``mu''
        :Exmample:
        >>> line = ...
        >>> p0 = line.point_on_line ( 0 ) ## should be equal to line.point 
        >>> p1 = line.point_on_line ( 1 ) ## shodul be equal to line.point+line.vector 
        """
        return self.point + mu * self.vector  
        
# =============================================================================
# 3D-Plane
# =============================================================================
class Plane3D(object) :
    """Planein 3D space
    """
    def __init__ ( self                            ,
                   point  = Point3D  ( 0  ,0 , 0 ) ,
                   normal = Vector3D ( 0 , 0 , 1 ) ) :
        
        if not isinstance ( point  ,  Point3D  ) :
            raise NotImplementedError("Plane3D: invalid ``point'' argument" )
        if not isinstance ( normal ,  Vector3D ) :
            raise NotImplementedError("Plane3D: invalid ``normal'' argument" )
        
        if 0 == normal.mag2  :
            raise ValueError ("Plane3D: ``normal'' must be zero!" )
            
        self.point  = Point3D .fromvector ( point  ) 
        self.normal = Vector3D.fromvector ( normal )  

    @classmethod
    def from_points ( cls , point1 , point2 , point3 ) :
        """Create the plane from three  points
        
        point1 : the first  point on the plane 
        point2 : the second point on the plane 
        point3 : the third  point on the plane

        """
        v21 = point2 - point1 
        v31 = point3 - point1 
        return cls ( point1 , v21.cross ( v31 ) ) 

    @classmethod
    def from_line_and_point ( cls , line , point ) :
        """Create the plane from the line and point 
        
        line   : the line in plane 
        point  : the point in plane 
        """
        return cls ( point1 ,  line.vector.cross ( point - line.point ) )  
    
    ## is the point or line on plane ? 
    def __contains__ ( self , obj ) :
        """Is the point or line on the line ?
        
        object : the point or line to be tested
        
        :Example:
        >>> line  = ...
        >>> point = ...
        >>> plane = ...
        >>> if point in plane : ...
        >>> if line  in plane : ...
        """
        return obj.on_plane ( self )

    def __repr__(self):
        """Simple class representation."""
        return "<Plane3D({0},{1})>".format( self.point , self.normal ) 

    def __str__(self):
        """Simple class representation."""
        return "Plane3D({0},{1})".format( self.point , self.normal ) 


# ===========================================================================
if '__main__' == __name__ :

    v = Vector3D( 1,2,3)
    p = Point3D( 1,2,3)
    print p,v
    p += 0.5*v
    print p
    p -= 0.5*v
    print p, p + v*4, p - ( p + v ) 
    
    line = Line3D ( p , v )
    print 'P in ilne:', p in line  

    line = Line3D.frompoints ( p , Point3D(3,2,1) )
    print 'P in ilne:', p in line  
    
    plane = Plane3D( p , v )
    print 'Line  in plane?', line in plane
    
    plane = Plane3D.frompoints ( p , Point3D(3,2,1) , Point3D(0,0,3) )
    print 'Point in plane?', p    in plane
    
    
    
# =============================================================================
#                                                                       The END 
# =============================================================================




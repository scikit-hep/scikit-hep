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
    'distance' , ## 3D-distance between geometry objects
    )
# =============================================================================
# Import statements
# =============================================================================
from skhep.math.vectors import Vector3D
from skhep.math.numeric import isequal
import numpy as np

# =============================================================================
# 3D-point
# =============================================================================
class Point3D(object) :
    """Point in 3D space.
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

        Parameters
        ----------
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

        Parameters
        ----------
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
        return self._vct.rho()

    @property
    def theta(self):
        """Return the spherical coordinate theta.
        """
        return self._vct.theta( )

    @property
    def phi(self):
        """Return the spherical or cylindrical coordinate phi.
        """
        return self._vct.phi( )

    def copy  ( self ) :
        """Make a copy of this point."""
        return Point3D( self[0], self[1],  self[2] )

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

    ## operations
    def __iadd__ ( self , vector ) :
        """Add vector to point.

        Example
        -------
        >>> p  = Point3D  ( ... )
        >>> v  = Vector3D ( ... )
        >>> p += v
        """

        if isinstance ( vector , Vector3D ) :
            self._vct += vector
            return self
        return NotImplemented

    def __isub__ ( self , vector ) :
        """Subtract vector from point.

        Example
        -------
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
        """Addition of point and vector.

        point + vector  --> point
        """
        ## point + vector = point
        if isinstance ( vector , Vector3D ) :
            newpoint  = self.copy()
            newpoint += vector
            return newpoint

        return NotImplemented

    def __sub__ (  self , other ) :
        """ Subtraction for points and vectors.

        1. point - point   -->  vector
        2. point - vector  -->  point
        """
        ## point - point  --> vector
        if isinstance ( other , Point3D ) : return self._vct - other._vct

        ## point - vector --> point
        if isinstance ( other , Vector3D ) :
            newpoint  = self.copy()
            newpoint -= other
            return newpoint

        return NotImplemented

    def __radd__ ( self , other )  :
        """Right addition of vector and point."""
        return self + other

    def __repr__(self):
        """Class representation."""
        return "<Point3D(x={0},y={1},z={2})>".format(self.x,self.y,self.z)

    def __str__(self):
        """Simple class representation."""
        return "Point3D(x={0},y={1},z={2})".format(self.x,self.y,self.z)

    def __eq__ ( self , other ) :
        """Equality  criteria for two points.

        Example
        -------
        >>> point1 = ...
        >>> point2 = ...
        >>> point1 == point2
        """
        if   isinstance ( other , Point3D ) :
            return np.all(self._vct == other._vct)
        elif isinstance ( other , ( float , int , long) ) :
            return np.all(self._vct == other)
        return NotImplemented

    def __ne__ ( self , other ) :
        """Non-equality  crietria for two points.

        Example
        -------
        >>> point1 = ...
        >>> point2 = ...
        >>> point1 != point2
        """
        return not  np.all( self == other )

    def on_line  ( self , line ) :
        """In the point on the line?"""
        v = line.point - self
        return 0 == v.mag2 or line.iscollinear  ( v )

    def on_plane ( self , plane ) :
        """Is the point on the plane?"""
        v = plane.point - self
        return 0 == v.mag2 or plane.normal.isperpendicular ( v )

    def distance ( self , other ) :
        """Get 'distance' between point  and other object.
        """
        if   isinstance ( other , Point3D ) :
            return abs ( self - other )
        elif isinstance ( other ,  ( Line3D , Plane3D ) ) :
            return other.distance ( self )
        raise NotImplementedError("Distance from Point3D to %s is not defined" % other )


# =============================================================================
# 3D-Line
# =============================================================================
class Line3D(object) :
    """Line in 3D space.
    Line is defined by a point on line and by the direction.
    """
    def __init__ ( self                            ,
                   point  = Point3D  ( 0  ,0 , 0 ) ,
                   vector = Vector3D ( 0 , 0 , 1 ) ) :

        if not isinstance ( point  ,  Point3D  ) :
            raise NotImplementedError("Line3D: invalid ``point'' argument" )
        if not isinstance ( vector ,  Vector3D ) :
            raise NotImplementedError("Line3D: invalid ``vector'' argument" )

        if 0 == vector.mag2  :
            raise ValueError ("Line3D: ``vector'' must not be zero!" )

        self.point     = point  .copy()
        self.direction = vector .copy()

    @classmethod
    def from_points ( cls , point1 , point2 ) :
        """Create the line from two points.

        Parameters
        ----------
        point1 : the first point on the line
        point2 : the second point on the line

        """
        return cls ( point1 , point2 - point1 )

    @classmethod
    def from_line   ( cls , line  ) :
        """Create the line from anoother line."""
        return cls ( line.point , line.direction )

    def __repr__(self):
        """Simple class representation."""
        return "<Line3D({0},{1})>".format( self.point , self.direction )

    def __str__(self):
        """Simple class representation."""
        return "Line3D({0},{1})".format( self.point , self.direction )

    def copy  ( self ) :
        """Make a copy of this line."""
        return Line3D( self.point.copy() , self.direction.copy() )

    ## is the point on line ?
    def __contains__ ( self , point ) :
        """Is the point on the line?

        Example
        -------
        >>> line  = ...
        >>> point = ...
        >>> if point in line : ...
        """
        return point.on_line ( self )

    def iscollinear ( self , other ) :
        """Is the line collinear to another line or vector?
        """
        if   isinstance ( other , Line3D   ) : other = other.direction
        elif isinstance ( other , Vector3D ) : pass
        else : raise TypeError("Line3D.iscollinear: invalid ``other'' argument" )
        ##
        return self.direction.iscollinear ( other  )

    def __eq__ ( self , other ) :
        """Equality  criteria for two lines.

        Example
        -------
        >>> line1 = ...
        >>> line2 = ...
        >>> print line1 == line2
        """
        return other.point in self  and self.iscollinear ( other )

    def __ne__ ( self , other ) :
        """Nonequality  criteria for two lines.

        Example
        -------
        >>> line1 = ...
        >>> line2 = ...
        >>> print line1 != line2
        """
        return not ( self  == other )

    def on_plane ( self , plane ) :
        """Is the line on the plane?
        """
        return self.point.on_plane ( plane ) and self.direction.isperpendicular ( plane.normal )

    def point_on_line (  self , mu ) :
        """ Get the point on line, that  corresponds to parameter 'mu'.

        Example
        -------
        >>> line = ...
        >>> p0 = line.point_on_line ( 0 ) ## should be equal to line.point
        >>> p1 = line.point_on_line ( 1 ) ## shodul be equal to line.point+line.vector
        """
        return self.point + mu * self.direction

    def closest_point_param ( self , point) :
        """Get the 'mu' parameter of the point on line that is closest to the given point in space.

        Example
        -------
        >>> line  = ...
        >>> point = ...
        >>> mu    = line.closest_point_param ( point )
        """
        return ( self.direction * ( self.point - point ) ) / self.direction.mag2

    def closest_points_params ( self , line ) :
        """Get the 'mu' parameters of two points on lines that is closest to each other.

        Example
        -------
        >>> line1 = ...
        >>> line2 = ...
        >>> mu1 , mu2  = line1.closest_points_param ( line2 )
        """
        a00  =  self.direction.mag2
        a01  =  self.direction * line.direction
        a10  = -a01
        a11  = -line.direction.mag2

        deti = a00 * a11 -  a01 * a10


        ## two lines are actually parallel
        if isequal ( deti , 0 , scale = abs ( a00 * a11) ) :
            return 0., line.closest_point_param ( self.point )

        detinv = 1.0/deti

        v  = line.point - self.point

        b0 = v * self.direction
        b1 = v * line.direction

        mu1 = (   a11 * b0 - a10 * b1 ) * detinv
        mu2 = (  -a01 * b0 + a00 * b1 ) * detinv

        return mu1 , mu2

    def closest_point  ( self , point ) :
        """Get the point on line that is closest to the given point in space.

        Example
        -------
        >>> line  = ...
        >>> point = ...
        >>> closest  = line.closest_point ( point )
        """
        return self.point_on_line ( self.closest_point_param ( point ) )

    def closest_points ( self , line ) :
        """Get two points on lines that is closest to each other.

        Example
        -------
        >>> line1 = ...
        >>> line2 = ...
        >>> p1 , p2  = line1.closest_points ( line2 )
        """
        mu1,mu2 = self.closest_points_params ( line )
        return self.point_on_line ( mu1 ), line.point_on_line ( mu2 )

    def distance ( self , other ) :
        """Get 'distance' between line and other object.

        Examples
        --------
        >>> line  = ...
        >>> point = ...
        >>> line2 = ...
        >>> plane = ...
        >>> print line.distance ( line2 )
        >>> print line.distance ( point )
        >>> print line.distance ( plane )
        """
        if   isinstance ( other , Point3D ) :
            if other in self : return 0
            return abs ( other -  self.closest_point ( other ) )
        elif isinstance ( other ,  Line3D ) :
            if other ==  self : return 0
            p1,p2 = self.closest_points ( other )
            return abs ( p1 - p2 )
        elif isinstance ( other , Plane3D ) :
            return other.distance ( self )

        raise NotImplementedError("Distance from Line3D to %s is not defined" % other )

    def angle ( self, other ) :
        """Get the 'angle' between a line and other object.
        """
        if   isinstance ( other ,  Line3D ) :
            return self.direction.angle ( other.direction )
        elif isinstance ( other , Plane3D ) :
            return self.direction.angle ( other.normal )

        raise NotImplementedError("Angle between a Line3D and a %s is not defined" % other )

    def intersect ( self, other ) :
        """Get the 'intersection' between a line and other object.
        """

        if isinstance ( other , Point3D ):
            if other in self:
                return other
            else:
                return None

        elif isinstance ( other , Line3D ):
            dist = self.distance ( other )

            if isequal ( dist, 0.0 ):
                return self.closest_points( other )[0]
            else:
                return None

        elif isinstance ( other , Plane3D ):

            if self.direction.isperpendicular ( other.normal):
                if self.on_plane ( other ):
                    return self
                else:
                    return None
            else:
                nom = other.normal * ( other.point - self.point )
                den = other.normal * ( self.direction )
                mu = nom / den

                return self.point_on_line ( mu )

        raise NotImplementedError("Intersection between a Line3D and a %s is not defined" % other )



# =============================================================================
# 3D-Plane
# =============================================================================
class Plane3D(object) :
    """Plane in 3D space, defined by a point on plane and by the normal vector.
    """
    def __init__ ( self                            ,
                   point  = Point3D  ( 0  ,0 , 0 ) ,
                   normal = Vector3D ( 0 , 0 , 1 ) ) :

        if not isinstance ( point  ,  Point3D  ) :
            raise NotImplementedError("Plane3D: invalid ``point'' argument" )
        if not isinstance ( normal ,  Vector3D ) :
            raise NotImplementedError("Plane3D: invalid ``normal'' argument" )

        if 0 == normal.mag2  :
            raise ValueError ("Plane3D: ``normal'' must not be zero!" )

        self.point     = point  .copy()
        self.normal    = normal .copy()

    @classmethod
    def from_points ( cls , point1 , point2 , point3 ) :
        """Create the plane from three  points.

        Parameters
        ----------
        point1 : the first  point on the plane
        point2 : the second point on the plane
        point3 : the third  point on the plane
        """
        v21 = point2 - point1
        v31 = point3 - point1
        return cls ( point1 , v21.cross ( v31 ) )

    @classmethod
    def from_line_and_point ( cls , line , point ) :
        """Create the plane from the line and point.

        Parameters
        ----------
        line   : the line in plane
        point  : the point in plane
        """
        return cls ( point ,  line.direction.cross ( point - line.point ) )

    ## is the point or line on plane ?
    def __contains__ ( self , obj ) :
        """Is the point or line on the line?

        Parameters
        ----------
        object : the point or line to be tested

        Example
        -------
        >>> line  = ...
        >>> point = ...
        >>> plane = ...
        >>> if point in plane : ...
        >>> if line  in plane : ...
        """
        return obj.on_plane ( self )

    def isparallel( self , other ) :
        """Is the plane collinear to another line, vector or plane?
        """
        if   isinstance ( other , Line3D   ) :
            return self.normal.isperpendicular ( other.direction )
        elif isinstance ( other , Vector3D ) :
            return self.normal.isperpendicular ( other )
        elif isinstance ( other , Plane3D ) :
            return self.normal.iscollinear ( other.normal )
        else : raise TypeError("Plane3D.isparallel: invalid ``other'' argument" )

    def __repr__(self):
        """Simple class representation."""
        return "<Plane3D({0},{1})>".format( self.point , self.normal )

    def __str__(self):
        """Simple class representation."""
        return "Plane3D({0},{1})".format( self.point , self.normal )

    def copy  ( self ) :
        """Make a copy of this plane.
        """
        return Plane3D( self.point.copy() , self.normal.copy() )


    def __eq__ ( self , other ) :
        """Equality  criteria for two planes.

        Example
        -------
        >>> plane1 = ...
        >>> plane2 = ...
        >>> print plane1 == plane2
        """
        return other.point in self  and self.normal.iscollinear ( other.normal )

    def __ne__ ( self , other ) :
        """Nonequality  criteria for two planes.

        Example
        -------
        >>> plane1 = ...
        >>> plane2 = ...
        >>> print plane1 != plane2
        """
        return not ( self  == other )

    def distance ( self , other ) :
        """Get 'distance' between plane and other object.

        Examples
        --------
        >>> line  = ...
        >>> point = ...
        >>> line2 = ...
        >>> plane = ...
        >>> print line.distance ( line2 )
        >>> print line.distance ( point )
        >>> print line.distance ( plane )
        """
        try:
            if   isinstance ( other , Point3D ) :
                if other in self : return 0
                v = other - self.point
                return   abs( v * self.normal ) / self.normal.mag

            elif self.isparallel ( other ) :
                return self.distance ( other.point )

            else : return 0

        except TypeError:
            raise NotImplementedError("Distance from Line3D to %s is not defined" % other )


    def angle ( self, other ) :
        """Get the 'angle' between a plane and other object.
        """
        if   isinstance ( other ,  Line3D ) :
            return self.normal.angle ( other.direction )
        elif isinstance ( other , Plane3D ) :
            return self.normal.angle ( other.normal )

        raise NotImplementedError("Angle between a Line3D and a %s is not defined" % other )

    def intersect ( self, other ) :
        """Get the 'intersection' between a line and other object
        """

        if isinstance ( other , Point3D ):
            if other in self:
                return other
            else:
                return None

        elif isinstance ( other , Line3D ):
            return other.intersect ( self )

        elif isinstance ( other , Plane3D ):

            if self.isparallel( other ):
                return None
            else:

                N1, N2 = self.normal, other.normal
                d1, d2 = N1 * self.point._vct, N2 * other.point._vct

                det = N1 * N1 * N2 * N2 - ( N1 * N2 )**2
                deti = 1.0 / det

                c1 = ( d1 * N2 * N2 - d2 * N1 * N1 ) * deti
                c2 = ( d1 * N2 * N2 - d2 * N1 * N1 ) * deti

                point = Point3D.fromvector ( c1 * N1 + c2 * N2 )
                direction = N1.cross( N2 )

                return Line3D( point, direction )

        raise NotImplementedError("Intersection between a Plane3D and a %s is not defined" % other )



# ===========================================================================
def distance ( obj1 , obj2 ) :
    """Calculate 3D-distance between two geometry objects (points, lines, planes).

    Examples
    --------
    >>> line1  = ...
    >>> line2  = ...
    >>> point1 = ...
    >>> point2 = ...
    >>> plane1 = ...
    >>> plane2 = ...
    >>> for o1 in ( line1, line2 , point1 , point2 , plane1 , plane2 ) :
    ...    for o2 in ( line1, line2 , point1 , point2 , plane1 , plane2 ) :
    ...        print distance ( o1 , o2 )
    """
    return obj1.distance ( obj2 )

# ===========================================================================
if '__main__' == __name__ :

    v = Vector3D( 1,2,3)
    p = Point3D( 1,2,3)
    p += 0.5*v
    p -= 0.5*v
    p, p + v*4, p - ( p + v )

    line = Line3D ( p , v )
    p in line

    line = Line3D.from_points ( p , Point3D(3,2,1) )
    p in line

    plane = Plane3D( p , v )
    line in plane

    plane = Plane3D.from_points ( p , Point3D(3,2,1) , Point3D(0,0,3) )
    p in plane

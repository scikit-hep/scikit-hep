# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Vector classes
==============

Two vector classes are available:

* ``Vector3D``     : a 3-dimensional vector.
* ``LorentzVector``: a Lorentz vector, i.e. a 4-dimensional Minkowski space-time vector
                     or a 4-momentum vector.
                     The metric is (-1,-1,-1,+1).
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import

from skhep.utils.py23 import *

from skhep.utils.exceptions import *

from math import sqrt, atan2, cos, sin, acos, degrees, log, pi, sinh

# -----------------------------------------------------------------------------
# Vector class in 3D
# -----------------------------------------------------------------------------
class Vector3D(object):
    """
    Vector class in 3 dimensions.

    Constructors:
        __init__(x=0., y=0., z=0.)
        origin()
        frompoint(x, y, z)
        fromvector(avector)
        fromsphericalcoords(r, theta, phi)
        fromcylindricalcoords(rho, phi, z)
        fromiterable(values)
    """

    def __init__(self, x=0., y=0., z=0.):
        """Default constructor.

        :Example:

        >>> v1 = Vector3D()
        >>> v1
        <Vector3D (x=0.0,y=0.0,z=0.0)>
        >>> v2 = Vector3D(1,2,3)
        >>> v2
        <Vector3D (x=1,y=2,z=3)>
        """
        self.__values = [x, y, z]

    @classmethod
    def origin(cls):
        """Shortcut constuctor for the origin (x=0.,y=0.,z=0.).
        Equivalent to the default constructor Vector3D().
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
        return self.__values[0]

    @x.setter
    def x(self, value):
        """Sets x, aka first coordinate at position 0."""
        self.__values[0] = value

    @property
    def y(self):
        """Return the y, aka second coordinate at position 1."""
        return self.__values[1]

    @y.setter
    def y(self, value):
        """Sets y, aka second coordinate at position 1."""
        self.__values[1] = value

    @property
    def z(self):
        """Return the z, aka third coordinate at position 2."""
        return self.__values[2]

    @z.setter
    def z(self, value):
        """Sets z, aka third coordinate at position 2."""
        self.__values[2] = value

    @property
    def rho(self):
        """Return the cylindrical coordinate rho."""
        return sqrt(self.x**2 + self.y**2)
        
    @property
    def r(self):
        """Return the spherical coordinate r."""
        return self.mag
         
    def costheta(self):
        """Return the cosinus of the spherical coordinate theta."""
        if self.x == 0. and self.y == 0.:
            return 1.
        costheta = self.z / self.mag
        return costheta

    def theta(self, deg=False):
        """Return the spherical coordinate theta.

        Options:
            deg : return the angle in degrees (default is radians)
        """
        theta = acos(self.costheta())
        return theta if not deg else degrees(theta)

    def phi(self, deg=False):
        """Return the spherical or cylindrical coordinate phi.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        phi = atan2(self.y, self.x)
        return phi if not deg else degrees(phi)

    def set(self, x, y, z):
        """Update the vector components all at once."""
        self.__values = [x, y, z]

    def __setitem__(self, i, value):
        """Update/set the ith vector component (commencing at 0, of course)."""
        try:
            self.__values[i] = value
        except IndexError:
            raise IndexError(
                'Vector3D is of length {0} only!'.format(len(self)))

    def __getitem__(self, i):
        """Get the ith vector component (commencing at 0, of course)."""
        try:
            return self.__values[i]
        except IndexError:
            raise IndexError( 'Vector3D is of length {0} only!'.format(len(self)))

    def tolist(self):
        """Return the vector as a list."""
        return list(self.__values)

    def __len__(self):
        """Length of the vector, i.e. the number of elements = 3."""
        return len(self.__values)

    @property
    def mag(self):
        """Magnitude, a.k.a. norm, of the vector."""
        return sqrt(self.mag2)

    @property
    def mag2(self):
        """Square of the magnitude, a.k.a. norm, of the vector."""
        return sum(v ** 2 for v in self.__values)

    def __abs__ ( self ) :
        """Get the absolute value for the vector
        >>> v = ...
        >>> a = abs(v)
        """
        return self.mag 
    
    def copy(self) :
        """Get a copy of the vector
        :Example:
        >>> v = ...
        >>> v1 = v.copy()
        """
        return Vector3D( self[0] , self[1] , self[2] ) 
    
    def unit(self):
        """Return the normalized vector, i.e. the unit vector along the direction of itself."""
        mag = self.mag
        if mag > 0. or mag != 1. :
            return Vector3D.fromiterable([v / mag for v in self.__values])
        else:
            return self

    def __iadd__(self, other):
        """(self)Addition with another vector, i.e. self+other.
        :Example:
        >>> v1  = ...
        >>> v2  = ...
        >>> v1 += v2  
        """
        if not isinstance ( other ,  Vector3D ) : 
            raise InvalidOperationError("invalid operation '+=' between a 'Vector3D' and a '{0}'".format(other.__class__.__name__))
        self.__values[0] += other.__values[0]
        self.__values[1] += other.__values[1]
        self.__values[2] += other.__values[2]
        return self

    def __isub__(self, other):
        """(self)Subtraction with another vector, i.e. self+other.
        :Example:
        >>> v1  = ...
        >>> v2  = ...
        >>> v1 -= v2  
        """
        if not isinstance ( other ,  Vector3D ) : 
            raise InvalidOperationError("invalid operation '-=' between a 'Vector3D' and a '{0}'".format(other.__class__.__name__)) 
        self.__values[0] -= other.__values[0]
        self.__values[1] -= other.__values[1]
        self.__values[2] -= other.__values[2]
        return self 

    def __add__(self, other):
        """Addition with another vector, i.e. self+other."""
        if not isinstance ( other ,  Vector3D ) : return NotImplemented
        v = self.copy()
        v+= other
        return v

    def __sub__(self, other):
        """Subtraction with another vector, i.e. self-other."""
        if not isinstance ( other ,  Vector3D ) : return NotImplemented
        v = self.copy()
        v-= other
        return v

    def __imul__(self, other):
        """Scaling of the vector by a number
        
        :Example:
        >>> v = ...
        >>> v *= 2 
        """
        if isinstance ( other , ( int , float ) ) :
            return Vector3D.fromiterable ( [v * other for v in self.__values ] )
        else:
            raise InvalidOperationError("invalid operation '*=' between a 'Vector3D' and a '{0}'".format(other.__class__.__name__))
                            
    def __itruediv__(self, number):
        """Scaling of the vector by a number
            
        :Example:
        >>> v  = ...
        >>> v /= 2 
        """
        if not isinstance ( number , ( int , float ) ) : 
            raise InvalidOperationError("invalid operation '/=' between a 'Vector3D' and a '{0}'".format(number.__class__.__name__))
        elif 0 == number : raise ZeroDivisionError 
        self *= ( 1.0/number )
        return self
        
    __idiv__ = __itruediv__
    
    def __mul__(self, other):
        """Multiplication of the vector by either another vector or a number.
        Multiplication of two vectors is equivalent to the dot product, see dot(...).
        Example:
        >>> v2 = v1 * 2
        >>> number = v1 * v3
        """
        if isinstance ( other ,  Vector3D ) :
            return self.dot(other)
        v = self.copy()
        v *= other
        return v
        
    def __rmul__(self, other):
        """Right multiplication of the vector by either another vector or a number."""
        return self.__mul__(other)
                
    def __truediv__(self, number):
        """Division of the vector by a number."""
        v = self.copy()
        v /= number
        return v

    __div__ = __truediv__
        
    def __eq__  ( self , other ) :
        """Equality to another vector, or, equality to zero
        :Example:
        >>> v1 = ...
        >>> v2 = ...
        >>> print v1 == v2
        >>> print v1 == 0  
        """
        from skhep.math.numeric import isequal

        ## comparsion with scalar zero, very useful  in practice
        if isinstance ( other , ( float , int , long ) ) and isequal ( other , 0 ) : 
            return isequal ( self[0] , 0 ) and isequal ( self[1] , 0 ) and isequal ( self[2] , 0 ) 
        elif not isinstance ( other , Vector3D) :
            return NotImplemented
        ##
        return isequal ( self[0] , other[0] ) and isequal ( self[1] , other[1] ) and isequal ( self[2] , other[2] )  

    def __ne__  (self, other) :
        """Non-equality to another vector
        :Example:
        >>> v1 = ...
        >>> v2 = ...
        >>> print v1 != v2 
        """
        return not ( self == other )

    def __nonzero__ ( self ) :
        """Nonzero  vector?
        :Example:
        >>> vct = ...
        >>> if vct : ...
        """
        return 0 != self.mag2

    __bool__ = __nonzero__
    
    def __iter__(self):
        """Iterator implementation for the vector components."""
        return self.__values.__iter__()

    def dot(self, other):
        """Dot product with another vector."""
        return sum(v1 * v2 for v1, v2 in zip(self.__values, other.__values))

    def cross(self, other ):
        """Cross product with another vector."""
        return Vector3D( self[1] * other[2] - self[2] * other[1],
                         self[2] * other[0] - self[0] * other[2],
                         self[0] * other[1] - self[1] * other[0]
                        )
                        
    def rotate(self, angle, *args):
        """Rotate vector by a given angle (in radians) around a given axis."""
        if len(args) == 1 and isinstance(args[0], Vector3D):
            ux, uy, uz = args[0].__values
        elif len(args) == 1 and len(args[0]) == 3:
            ux, uy, uz = args[0]
        elif len(args) == 3:
            ux, uy, uz = args
        else:
            raise TypeError('Input object not a Vector3D nor an iterable with 3 elements.')

        for i, u in enumerate((ux, uy, uz)):
            if not isinstance( u, (int,float) ):
                raise ValueError( 'Component #{0} is not a number!'.format(i) )
             
        norm = sqrt(ux**2 + uy**2 + uz**2)
        if norm != 1.0:
            ux = ux / norm; uy = uy / norm; uz = uz / norm;
        c, s = cos(angle), sin(angle)
        c1 = 1. - c

        xp = (c + ux**2 * c1) * self.x + (ux * uy * c1 - uz * s) * self.y \
            + (ux * uz * c1 + uy * s) * self.z
        yp = (ux * uy * c1 + uz * s) * self.x + (c + uy**2 * c1) * self.y \
            + (uy * uz * c1 - ux * s) * self.z
        zp = (ux * uz * c1 - uy * s) * self.x + (uy * uz * c1 + ux * s) * self.y \
            + (c + uz**2 * c1) * self.z 
            
        return Vector3D(xp, yp, zp)
        
    def rotatex(self, angle):
        """Rotate vector by a given angle (in radians) around the x axis."""
        return self.rotate(angle, 1, 0, 0)
        
    def rotatey(self, angle):
        """Rotate vector by a given angle (in radians) around the y axis."""
        return self.rotate(angle, 0, 1, 0)
        
    def rotatez(self, angle):
        """Rotate vector by a given angle (in radians) around the z axis."""
        return self.rotate(angle, 0, 0, 1)
    
    def cosdelta ( self , other ) :
        """Get cos(angle) with respect to another vector
        """
        m1 = self.mag2
        if 0 >= m1 : return 1.0
        m2 = other.mag2
        if 0 >= m2 : return 1.0
        
        r = self.dot( other ) / sqrt ( m1 * m2 ) 
        return max ( -1.0 , min ( 1.0 , r ) )
    
        
    def angle(self, other, deg=False):
        """Angle with respect to another vector.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        cd = self.cosdelta ( other ) 
        return acos(cd) if not deg else degrees(acos(cd))

    def isparallel(self, other):
        """Check if another vector is parallel.
        Two vectors are parallel if they have the same direction but not necessarily the same magnitude.
        """
        from skhep.math.numeric import isequal
        return isequal ( self.cosdelta(other)  , 1 ) 

    def isantiparallel(self, other):
        """Check if another vector is antiparallel.
        Two vectors are antiparallel if they have opposite direction but not necessarily the same magnitude.
        """
        from skhep.math.numeric import isequal
        return isequal ( self.cosdelta(other) , -1 ) 

    def iscollinear ( self , other ) :
        """Check if another vector is collinear
        Two vectors are collinear if they have parallel or antiparallel
        """
        from skhep.math.numeric import isequal
        return isequal ( abs ( self.cosdelta ( other ) ) , 1 ) 
    
    def isopposite ( self , other):
        """Two vectors are opposite if they have the same magnitude but opposite direction."""
        from skhep.math.numeric import isequal
        added = self + other
        return added == 0

    def isperpendicular(self, other):
        """Check if another vector is perpendicular."""
        from skhep.math.numeric import isequal
        return isequal ( self.dot ( other ) , 0 , scale = max( self.mag2 , other.mag2 ) ) 

    def __repr__(self):
        """Class representation."""
        return "<Vector3D (x={0},y={1},z={2})>".format(*self.__values)

    def __str__(self):
        """Simple class representation."""
        return str(tuple(self.__values))

#-----------------------------------------------------------------------------
# Lorentz vector class
#-----------------------------------------------------------------------------
class LorentzVector(object):
    """
    Class representing a Lorentz vector,
    either a 4-dimensional Minkowski space-time vector or a 4-momentum vector.
    The 4-vector components can be seen as (x,y,z,t) or (px,py,pz,E).

    Constructors:
        __init__(x=0., y=0., z=0., t=0.)
        from4vector(avector)
        from3vector(vector3d, t)
    """
    def __init__(self, x=0., y=0., z=0., t=0.):
        """Default constructor.

        :Example:

        >>> v1 = LorentzVector()
        >>> v1
        """
        self.__vector3d = Vector3D(x, y, z)
        self.__t = t
        

    @classmethod
    def from4vector(cls, other):
        """Copy constructor."""
        return cls(other.x, other.y, other.z, other.t)

    @classmethod
    def from3vector(cls, vector3d, t):
        """Constructor from a Vector3D and the time/energy component."""
        return cls(vector3d.x, vector3d.y, vector3d.z, t)
        
    @classmethod
    def fromiterable(cls, values):
        """Constructor from a suitable iterable object.
        Suitable means here that all entries are numbers
        and the length equals 4.
        """
        values = list(values)
        if not len(values)==4:
            raise ValueError( 'Input iterable length = {0}! Please check your inputs.'.format(len(values)) )
        for i, v in enumerate(values):
            if not isinstance( v, (int,float) ):
                raise ValueError( 'Component #{0} is not a number!'.format(i) )
        return cls(values[0], values[1], values[2], values[3])

    @property
    def x(self):
        """Return the coordinate x, aka first coordinate at position 0."""
        return self.__vector3d.x

    @x.setter
    def x(self, value):
        """Sets x, aka first coordinate at position 0."""
        self.__vector3d.x = value

    @property
    def y(self):
        """Return the coordinate x, aka second coordinate at position 1."""
        return self.__vector3d.y

    @y.setter
    def y(self, value):
        """Sets y, aka second coordinate at position 1."""
        self.__vector3d.y = value

    @property
    def z(self):
        """Return the coordinate z, aka third coordinate at position 2."""
        return self.__vector3d.z

    @z.setter
    def z(self, value):
        """Sets z, aka third coordinate at position 2."""
        self.__vector3d.z = value
        
    @property
    def vector(self):
        """Return a copy of the vector of spatial components."""
        return self.__vector3d.copy()

    @property
    def t(self):
        """Return the time/energy component, aka coordinate at position 3."""
        return self.__t

    @t.setter
    def t(self, value):
        """Sets t, aka coordinate at position 3."""
        self.__t = value
        
    def costheta(self):
        """Return the cosinus of the spherical coordinate theta."""
        return self.__vector3d.costheta()

    def theta(self, deg=False):
        """Return the spherical coordinate theta.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        return self.__vector3d.theta(deg)

    def phi(self, deg=False):
        """Return the spherical or cylindrical coordinate phi.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        return self.__vector3d.phi(deg)

    @property
    def px(self):
        """Return the Vector3D coordinate px, aka first momentum coordinate at position 0."""
        return self.__vector3d.x

    @px.setter
    def px(self, value):
        """Sets px, aka first momentum coordinate at position 0."""
        self.__vector3d.x = value

    @property
    def py(self):
        """Return the Vector3D coordinate px, aka second momentum coordinate at position 1."""
        return self.__vector3d.y

    @py.setter
    def py(self, value):
        """Sets py, aka second momentum coordinate at position 1."""
        self.__vector3d.y = value

    @property
    def pz(self):
        """Return the Vector3D coordinate pz, aka third momentum coordinate at position 2."""
        return self.__vector3d.z

    @pz.setter
    def pz(self, value):
        """Sets pz, aka third momentum coordinate at position 2."""
        self.__vector3d.z = value

    @property
    def e(self):
        """Return the energy/time component, aka momentum coordinate at position 3."""
        return self.__t
        
    @e.setter
    def e(self, value):
        """Sets e, aka momentum coordinate at position 3."""
        self.__t = value
        
    def set(self, x, y, z, t):
        """Update/set all components at once."""
        self.__vector3d = Vector3D(x, y, z)
        self.__t = t
        
    def setpxpypzm(self, px, py, pz, m):
        """Set the px,py,pz components and the mass."""
        self.__vector3d.x = px; self.__vector3d.y = py; self.__vector3d.z = pz
        if m > 0.:
            self.__t = sqrt(px**2 + py**2 + pz**2 + m**2)
        else:
            self.__t = sqrt(px**2 + py**2 + pz**2 - m**2)
            
    def setpxpypze(self, px, py, pz, e):
        """Set the px,py,pz components and the energy."""
        self.set(px,py,pz,e)
        
    def setptetaphim(self, pt, eta, phi, m):
        """ Set the transverse momentum, the pseudorapidity, the angle phi and the mass."""
        px, py, pz = pt*cos(phi), pt*sin(phi), pt*sinh(eta)
        self.setpxpypzm(px,py,pz,m)
        
    def setptetaphie(self, pt, eta, phi, e):
        """ Set the transverse momentum, the pseudorapidity, the angle phi and the energy."""
        px, py, pz = pt*cos(phi), pt*sin(phi), pt*sinh(eta)
        self.setpxpypze(px,py,pz,e)
        
    def tolist(self):
        """Return the LorentzVector as a list."""
        return list(self.__vector3d) + [self.__t]
        
    def __setitem__(self, i, value):
        """Update/set the ith vector component (commencing at 0, of course)."""
        try:
            if i == 3: self.__t = value
            else: self.__vector3d[i] = value
        except IndexError:
            raise IndexError(
                'LorentzVector is of length {0} only!'.format(len(self)))

    def __getitem__(self, i):
        """Get the ith vector component (commencing at 0, of course)."""
        try:
            return self.tolist()[i]
        except IndexError:
            raise IndexError( 'LorentzVector is of length {0} only!'.format(len(self)))

    def __len__(self):
        """Length of the LorentzVector, i.e. the number of elements = 4."""
        return len(self.tolist())
        
    @property
    def p(self):
        """Return the momentum, aka norm of the momentum vector."""
        return self.__vector3d.mag
        
    @property
    def pt(self):
        """Return the transverse momentum, aka transverse component of the momentum vector."""
        return self.perp
        
    @property
    def et(self):
        """Return the transverse energy."""
        return self.e * ( self.pt / self.p )

    @property
    def m(self):
        """Return the invariant mass."""
        return self.mag

    @property
    def m2(self):
        """Return the square of the invariant mass."""
        return self.mag2
        
    @property
    def mass(self):
        """Return the invariant mass."""
        return self.mag

    @property
    def mass2(self):
        """Return the square of the invariant mass."""
        return self.mag2
        
    @property  
    def mt(self):
        """Return the transverse mass."""
        return self.transversemass
    
    @property    
    def mt2(self):
        """Return the square of the transverse mass."""
        return self.transversemass2

    @property
    def transversemass(self):
        """Return the transverse mass."""
        mt2 = self.transversemass2
        return sqrt(mt2) if mt2 >= 0. else -sqrt(-mt2)
     
    @property   
    def transversemass2(self):
        """Return the square of the transverse mass."""
        return self.e**2 - self.pz**2

    @property
    def beta(self):
        """Return :math:`\\beta = v/c`."""
        return self.p / self.e

    @property
    def gamma(self):
        """Return :math:`\\gamma = 1/\\sqrt{1-\\beta^2}`."""
        if self.beta < 1:
            return 1. / sqrt(1. - self.beta**2)
        else:
            return 10E10

    @property
    def eta(self):
        """Return the pseudorapidity."""
        if abs(self.costheta()) < 1.:
            return -0.5 * log( (1. - self.costheta())/(1. + self.costheta()) )
        else:
            return 10E10 if self.z > 0 else -10E10
     
    @property       
    def boostvector(self):
        """Return the spatial component divided by the time component."""
        return Vector3D(self.x / self.t, self.y / self.t, self.z / self.t)

    @property
    def pseudorapidity(self):
        """"Return the pseudorapidity. Alternative to eta() method."""
        return self.eta

    @property
    def rapidity(self):
        """Return the rapidity."""
        return 0.5 * log( (self.e + self.pz)/(self.e - self.pz) )

    @property
    def mag(self):
        """Magnitude, a.k.a. norm, of the Lorentz vector."""
        mag2 = self.mag2
        return sqrt(mag2) if mag2 >= 0. else -sqrt(-mag2)

    @property
    def mag2(self):
        """Square of the magnitude, a.k.a. norm, of the Lorentz vector."""
        return self.t**2 - self.__vector3d.mag2
                
    @property
    def perp2(self):
        """Square of the transverse component, in the (x,y) plane, of the spatial components."""
        return self.x**2 + self.y**2
        
    @property
    def perp(self):
        """Transverse component of the spatial components."""
        return sqrt(self.perp2)

    def copy(self) :
        """Get a copy of the LorentzVector
        :Example:
        >>> v = ...
        >>> v1 = v.copy()
        """
        return LorentzVector( self[0] , self[1] , self[2] , self[3] ) 
        
    def __iadd__(self, other):
        """(self)Addition with another LorentzVector, i.e. self+other.
        :Example:
        >>> v1  = ...
        >>> v2  = ...
        >>> v1 += v2  
        """
        if not isinstance ( other ,  LorentzVector ) : 
            raise InvalidOperationError("invalid operation '+=' between a 'LorentzVector' and a '{0}'".format(other.__class__.__name__))
        self.__vector3d += other.__vector3d
        self.__t += other.__t
        return self 

    def __isub__(self, other):
        """(self)Subtraction with another LorentzVector, i.e. self+other.
        :Example:
        >>> v1  = ...
        >>> v2  = ...
        >>> v1 -= v2  
        """
        if not isinstance ( other ,  LorentzVector ) : 
            raise InvalidOperationError("invalid operation '-=' between a 'LorentzVector' and a '{0}'".format(other.__class__.__name__))
        self.__vector3d -= other.__vector3d
        self.__t -= other.__t
        return self

    def __add__(self, other):
        """Addition with another LorentzVector, i.e. self+other."""
        v = self.copy()
        v+= other
        return v 

    def __sub__(self, other):
        """Subtraction with another LorentzVector, i.e. self-other."""
        v = self.copy()
        v-= other
        return v 

        
    def __imul__(self, other):
        """Scaling of the LorentzVector with a number
        
        :Example:
        >>> v = ...
        >>> v *= 2 
        """
        if isinstance ( other , ( int , float ) ) :
            return LorentzVector.fromiterable ( [v * other for v in self.tolist() ] )
        else:
            raise InvalidOperationError("invalid operation '*=' between a 'LorentzVector' and a '{0}'".format(other.__class__.__name__))
        
    def __itruediv__(self, number):
        """Scaling of the LorentzVector with a number
        
        :Example:
        >>> v  = ...
        >>> v /= 2 
        """
        if not isinstance ( number , ( int , float ) ) : 
            raise InvalidOperationError("invalid operation '/=' between a 'LorentzVector' and a '{0}'".format(number.__class__.__name__))
        elif 0 == number : raise ZeroDivisionError 
        self *= ( 1.0/number )
        return self
        
    __idiv__ = __itruediv__

    def __mul__(self, other):
        """Multiplication of the LorentzVector by either another LorentzVector or a number.
        Multiplication of two LorentzVector is equivalent to the dot product, see dot(...).
        Example:
        >>> v2 = v1 * 2
        >>> number = v1 * v3
        """        
        if isinstance ( other , LorentzVector ):
            return self.dot(other)
        v = self.copy()
        v *= other
        return v
        
    def __rmul__(self, other):
        """Right multiplication of the LorentzVector by either another LorentzVector or a number."""
        return self.__mul__(other)
        
    def __truediv__(self, number):
        """Division of the LorentzVector by a number."""
        v = self.copy()
        v /= number
        return v
     
    __div__ = __truediv__
                
    def __eq__  ( self , other ) :
        """Equality to another LorentzVector, or, equality to zero
        :Example:
        >>> v1 = ...
        >>> v2 = ...
        >>> print v1 == v2
        >>> print v1 == 0  
        """
        from skhep.math.numeric import isequal

        ## comparsion with scalar zero, very useful  in practice
        if isinstance ( other , ( float , int , long ) ) and isequal ( other , 0 ) : 
            return isequal ( self[0] , 0 ) and isequal ( self[1] , 0 ) and isequal ( self[2] , 0 ) \
             and isequal ( self[3] , 0 )
        elif not isinstance ( other , LorentzVector ) :
            return NotImplemented
        ##
        return isequal ( self[0] , other[0] ) and isequal ( self[1] , other[1] ) and isequal ( self[2] , other[2] ) \
         and isequal ( self[3] , other[3] )

    def __ne__  (self, other) :
        """Non-equality to another Lorentz Vector
        :Example:
        >>> v1 = ...
        >>> v2 = ...
        >>> print v1 != v2 
        """
        return not ( self == other )

    def __iter__(self):
        """Iterator implementation for the Lorentz Vector components."""
        return self.tolist().__iter__()
        
    def boost(self, *args):
        """Apply a Lorentz boost on the Lorentz Vector."""
        if len(args) == 1 and isinstance(args[0], Vector3D):
            bx, by, bz = args[0].x, args[0].y, args[0].z
        elif len(args) == 1 and len(args[0]) == 3:
            bx, by, bz = args[0]
        elif len(args) == 3:
            bx, by, bz = args
        else:
            raise TypeError('Input object not a Vector3D nor an iterable with 3 elements.')

        for i, b in enumerate((bx, by, bz)):
            if not isinstance( b, (int,float) ):
                raise ValueError( 'Component #{0} is not a number!'.format(i) )
            
        b2 = bx**2 + by**2 + bz**2
        gamma = 1. / sqrt( 1. - b2 )
        bp = bx * self.x + by * self.y + bz * self.z
        if b2 > 0.:
            gamma2 = ( gamma - 1. ) / b2
        else:
            gamma2 = 0.
            
        xp = self.x + gamma2 * bp * bx - gamma * bx * self.t
        yp = self.y + gamma2 * bp * by - gamma * by * self.t
        zp = self.z + gamma2 * bp * bz - gamma * bz * self.t
        tp = gamma * ( self.t - bp )
            
        return LorentzVector(xp, yp, zp, tp)
        
    def rotate(self, angle, *args):
        """Rotate vector by a given angle (in radians) around a given axis."""
        
        v3p = self.__vector3d.rotate(angle, *args)
        
        return LorentzVector().from3vector(v3p, self.t)
        
    def rotatex(self, angle):
        """Rotate vector by a given angle (in radians) around the x axis."""
        return self.rotate(angle, 1, 0, 0)
        
    def rotatey(self, angle):
        """Rotate vector by a given angle (in radians) around the y axis."""
        return self.rotate(angle, 0, 1, 0)
        
    def rotatez(self, angle):
        """Rotate vector by a given angle (in radians) around the z axis."""
        return self.rotate(angle, 0, 0, 1)
        
    def dot(self, other):
        """Dot product with another Lorentz Vector."""
        return self.t * other.t - self.__vector3d * other.__vector3d
        
    def deltaeta(self, other):
        """Return the pseudorapidity difference, :math:`\\Delta \\eta`, with another Lorentz vector."""
        return self.eta - other.eta
        
    def deltaphi(self, other):
        """Return the phi angle difference, :math:`\\Delta \\phi`, with another Lorentz vector."""
        dphi = self.phi() - other.phi()
        while dphi > pi: 
            dphi -= 2*pi
        while dphi < -pi:
            dphi += 2*pi
        return dphi
        
    def deltar(self, other):
        """Return :math:`\\Delta R` the distance in (eta,phi) space with another Lorentz vector, defined as:
            :math:`\\Delta R = \\sqrt{(\\Delta \\eta)^2 + (\\Delta \\phi)^2}`
        """
        return sqrt( self.deltaeta(other)**2 + self.deltaphi(other)**2 )

    def isspacelike(self):
        """Check if Lorentz Vector is space-like."""
        from skhep.math.numeric import isequal
        return self.mag2 < 0. and not isequal(self.mag2, 0.)

    def istimelike(self):
        """Check if Lorentz Vector is time-like."""
        from skhep.math.numeric import isequal
        return self.mag2 > 0. and not isequal(self.mag2, 0.)

    def islightlike(self):
        """Check if Lorentz Vector is light-like."""
        from skhep.math.numeric import isequal
        return isequal(self.mag2, 0.)

    def __repr__(self):
        """Class representation."""
        return "<LorentzVector (x={0},y={1},z={2},t={3})>".format(*self.tolist())
    
    def __str__(self):
        """Simple class representation."""
        return str(tuple(self.tolist()))

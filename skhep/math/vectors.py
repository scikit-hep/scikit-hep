# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Vector classes
==============

Two vector classes are available:

* Vector3D     : a 3-dimensional vector
* LorentzVector: a Lorentz vector
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function

from math import sqrt, atan2, cos, sin, acos, degrees


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
        return cls(other.x(), other.y(), other.z())

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
        if not len(values) == 3:
            print('Input iterable length = {0}! Please check your inputs.'.format(
                len(values)))
            return None
        for i, v in enumerate(values):
            if not isinstance(v, (int, float)):
                print('Component #{0} is not a number!'.format(i))
                return None
        return cls(values[0], values[1], values[2])

    def x(self):
        """Return the x, aka first coordinate at position 0."""
        return self.__values[0]

    def y(self):
        """Return the x, aka second coordinate at position 1."""
        return self.__values[1]

    def z(self):
        """Return the x, aka third coordinate at position 2."""
        return self.__values[2]

    def rho(self):
        """Return the cylindrical coordinate rho."""
        return sqrt(self.x() ** 2 + self.y() ** 2)

    def theta(self, deg=False):
        """Return the spherical coordinate theta.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        raise NotImplementedError

    def phi(self, deg=False):
        """Return the spherical or cylindrical coordinate phi.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        if self.x() == 0 and self.y() == 0:
            return 0.
        phi = atan2(self.y(), self.x())
        return phi if not deg else degrees(phi)

    def set(self, x, y, z):
        """Update the vector components all at once."""
        self.__values = [x, y, z]

    def setx(self, x):
        """Update/set the x component."""
        self.__values[0] = x

    def sety(self, y):
        """Update/set the y component."""
        self.__values[1] = y

    def setz(self, z):
        """Update/set the z component."""
        self.__values[2] = z

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
            print('Vector3D is of length {0} only!'.format(len(self)))
            return None

    def tolist(self):
        """Return the vector as a list."""
        return list(self.__values)

    def __len__(self):
        """Length of the vector, i.e. the number of elements = 3."""
        return len(self.__values)

    def mag(self):
        """Magnitude, a.k.a. norm, of the vector."""
        return sqrt(self.mag2())

    def mag2(self):
        """Square of the magnitude, a.k.a. norm, of the vector."""
        return sum(v ** 2 for v in self.__values)

    def unit(self):
        """Return the normalized vector, i.e. the unit vector along the direction of itself."""
        mag = self.mag()
        if mag > 0.:
            return Vector3D.fromiterable([v / mag for v in self.__values])
        else:
            return self

    def perpendicular(self):
        """Return the vector perpendicular to itself."""
        raise NotImplementedError

    def __add__(self, other):
        """Addition with another vector, i.e. self+other."""
        return Vector3D.fromiterable([v1 + v2 for v1, v2 in zip(self.__values, other.__values)])

    def __sub__(self, other):
        """Subtraction with another vector, i.e. self-other."""
        return Vector3D.fromiterable([v1 - v2 for v1, v2 in zip(self.__values, other.__values)])

    def __mul__(self, other):
        """Multiplication of the vector by either another vector or a number.
        Multiplication of two vectors is equivalent to the dot product, see dot(...).

        Example:
        >>> v2 = v1 * 2
        >>> number = v1 * v3
        """
        if isinstance(other, (int, float)):
            return Vector3D.fromiterable([v * other for v in self.__values])
        elif isinstance(other, Vector3D):
            return self.dot(other)
        else:
            print('Input object not a vector nor a number! Cannot multiply.')
            return None

    def __rmul__(self, other):
        """Right multiplication of the vector by either another vector or a number."""
        return self.__mul__(other)

    def __div__(self, number):
        """Division of the vector by a number."""
        if not isinstance(number, (int, float)):
            print('Argument is not a number!')
            return None
        if number == 0.:
            raise ZeroDivisionError
        return Vector3D.fromiterable([v / number for v in self.__values])

    def __iter__(self):
        """Iterator implementation for the vector components."""
        return self.__values.__iter__()

    def dot(self, other):
        """Dot product with another vector."""
        return sum(v1 * v2 for v1, v2 in zip(self.__values, other.__values))

    def cross(self, v1, v2):
        """Cross product with another vector."""
        return Vector3D(v1[1] * v2[2] - v1[2] * v2[1],
                        v1[2] * v2[0] - v1[0] * v2[2],
                        v1[0] * v2[1] - v1[1] * v2[0]
                        )

    def angle(self, other, deg=False):
        """Angle with respect to another vector.

        Options:
           deg : return the angle in degrees (default is radians)
        """
        prod_mag2 = self.mag2() * other.mag2()
        if prod_mag2 <= 0.:
            return 0.
        else:
            arg = self.dot(other) / sqrt(prod_mag2)
            if arg > 1.:
                arg = 1.
            if arg < -1.:
                arg = -1.
            return acos(arg) if not deg else degrees(acos(arg))

    def isparallel(self, other):
        """Check if another vector is parallel.
        Two vectors are parallel if they have the same direction but not necessarily the same magnitude.
        """
        return cos(self.angle(other)) == 1.

    def isantiparallel(self, other):
        """Check if another vector is antiparallel.
        Two vectors are antiparallel if they have opposite direction but not necessarily the same magnitude.
        """
        return cos(self.angle(other)) == -1.

    def isopposite(self, other):
        """Two vectors are opposite if they have the same magnitude but opposite direction."""
        added = self + other
        return added.x() == 0 and added.y() == 0 and added.z() == 0

    def isperpendicular(self, other):
        """Check if another vector is perpendicular."""
        return self.dot(other) == 0.

    def __repr__(self):
        """Class representation."""
        return "<Vector3D (x={0},y={1},z={2})>".format(self.__values[0], self.__values[1], self.__values[2])

    def __str__(self):
        """Simple class representation."""
        return str(tuple(self.__values))

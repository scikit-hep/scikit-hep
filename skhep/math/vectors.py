# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Vector classes
==============

Three vector classes are available:

* ``Vector2D``     : a 2-dimensional vector.
* ``Vector3D``     : a 3-dimensional vector.
* ``LorentzVector``: a Lorentz vector, i.e. a 4-dimensional Minkowski space-time vector
                     or a 4-momentum vector.
                     The metric is (-1,-1,-1,+1).

These are based on the base class ``Vector``, this can be subclassed to make new vectors with new metrics.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
from __future__ import division, print_function, absolute_import

import numpy as np
import doctest
from .numbautils import overload

# -----------------------------------------------------------------------------
# Vector class (base)
# -----------------------------------------------------------------------------

def _add_names(cls):
    for n,x in enumerate(cls.NAMES):
        # Add .x, .y, etc. property setters/getters
        def make_get_set(n):
            def getter(self):
                return self[n].view(np.ndarray)
            def setter(self, item):
                self[n] = item
            return getter, setter
        setattr(cls, x, property(*make_get_set(n)))

        # Add X, Y, etc basis vectors
        ze = [0]*len(cls.NAMES)
        ze[n] = 1
        setattr(cls, x.upper(), cls(*ze))


class Vector(np.ndarray):
    # All valid subclasses must have NAMES in class
    __slots__ = ()

    def __new__(cls, *args, **kargs):

        dtype=kargs.get('dtype', np.double)

        if len(args)==0:
            args = np.zeros(len(cls.NAMES))
        args = [np.asarray(a).astype(dtype) for a in args]
        args = np.broadcast_arrays(*args)
        if hasattr(np, 'stack'): # Support 1.08, but 1.10 is better
            return np.stack(args).view(cls)
        else:
            args = [np.expand_dims(a,0) for a in args]
            return np.concatenate(args,0).view(cls)

    # Special constructors

    @classmethod
    def origin(cls):
        """Shortcut constuctor for the origin (x=0.,y=0., ...).
        Equivalent to the default constructor.
        """
        return cls()

    @classmethod
    def from_pandas(cls, pd_dataframe):
        items = (pd_dataframe[n] for n in cls.NAMES)
        return cls(*items)

    @classmethod
    def from_vector(cls, other):
        """Copy constructor."""
        return cls(*other)

    # Not including fromiterable because it is available directly as Vector(*iterable)

    def dot(self, other):
        '''
        This currently returns a 1D array always.

        >>> v1 = Vector3D(1, 2, 3)
        >>> v2 = Vector3D(2, 3, 5)
        >>> v1p = Vector3D([1,2,3], [2,3,5], [3,3,1])
        >>> v2p = Vector3D([1,2,3], [3,5,2], [5,3,2])
        >>> v1.dot(v2)
        array([ 23.])
        >>> v1p.dot(v2p)
        array([ 22.,  28.,  21.])
        '''

        if hasattr(self.__class__, 'METRIC'):
            metric = self.METRIC.copy()
            for axis in range(len(self.shape) - 1):
                metric = np.expand_dims(metric, -1)
            return np.sum((self*metric) * other, 0).view(np.ndarray)
        else:
            return np.sum(self * other, 0).view(np.ndarray)


    def mag(self):
        '''
        This currently returns a 1D array always.

        >>> v1 = Vector3D(1, 2, 3)
        >>> v1p = Vector3D([1,2,3], [2,3,5], [3,3,1])
        >>> np.all(v1.mag() == np.sqrt(14))
        True
        >>> v1p.mag()
        array([ 3.74165739,  4.69041576,  5.91607978])
        '''

        return np.sqrt(np.abs(self.mag2()).view(np.ndarray))*np.sign(self.mag2())

    def mag2(self):
        '''
        >>> v1 = Vector3D(1, 2, 3)
        >>> v1p = Vector3D([1,2,3], [2,3,5], [3,3,1])
        >>> np.all(v1.mag2() == 14)
        True
        >>> v1p.mag2()
        array([ 14.,  22.,  35.])

        >>> v = LorentzVector(1,2,3,.5)
        >>> v.mag2()
        array([-13.75])
        '''
        return self.dot(self)

    def unit(self, inplace=False):
        if inplace:
            self /= self.mag()
        else:
            return self / self.mag()


    @property
    def T(self):
        return super(Vector, self).T.view(np.ndarray)
    @T.setter
    def T(self, val):
        super(Vector, self).T = val

    def to_pd(self):
        '''Support for easy conversion to pandas'''
        import pandas as pd
        return pd.DataFrame({name:getattr(self, name) for name in self.NAMES})

    def angle(self, other, normal=None):
        'Angle between vectors, might not be normalized.'
        a = self.unit()
        b = other.unit()
        # Protection vs. round off error
        ang = np.arccos(np.clip(a.dot(b),-1,1))
        # Only defined for Vector3
        if normal is not None:
            ang *= np.sign(normal.dot(a.cross(b)))
        return ang

    def __array_finalize__(self, obj):
        if self.shape[0] != len(self.NAMES):
            raise RuntimeError("Vectors must have the correct number of elements in the first diminsion, expected {0}, got {1}".format(len(self.NAMES), self.shape))

    def __array_wrap__(self, out_arr, context=None):
        "Correctly handle ufuncts"
        if len(out_arr.shape) == 0 or out_arr.shape[0] != len(self.NAMES):
            out_arr = out_arr.view(np.ndarray)
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __getitem__(self, item):
        'I have chosen for x and [0] to be the same, to simplify calcs (a lot)'
        if (isinstance(item, tuple)
            and len(item)>0
            and ((isinstance(item[0], slice)
                 and item[0] == slice(None,None,None)
                 ) or (
            len(item) < len(self.shape)
            and item[0] is Ellipsis))):
            # If [:,...] then keep vector
            return super(Vector,self).__getitem__(item)
        elif isinstance(item, slice) and item == slice(None,None,None):
            return super(Vector,self).__getitem__(item)
        else:
            return self.view(np.ndarray).__getitem__(item)

    def __setitem__(self, item, value):
        self.view(np.ndarray).__setitem__(item, value)

    @property
    def dims(self):
        return len(self.__class__.NAMES)

    def _repr_html_(self):
        shape = self.shape[1:]
        shape_txt = " x ".join(map(str,shape))
        vals = np.reshape(self, (self.dims,-1))
        len_v = max(sum(shape),1)

        header = r"<h3> {0} ({1}) </h3>".format(self.__class__.__name__, shape_txt)
        header += "<table>"
        header += "<tr>"
        for name in self.__class__.NAMES:
            header += r"<td><b>{}</b></td>".format(name)
        header += r"</tr>"
        content = ""
        for i in range(min(len_v,5)):
            content += "<tr>"
            for name in self.__class__.NAMES:
                content += r"<td>{:.4}</td>".format(getattr(vals,name)[i])
            content += r"</tr>"

        if len_v > 5:
            for name in self.__class__.NAMES:
                content += r"<td> &#8226; &#8226; &#8226; </td>"
        footer = r"</table>"
        return header + content + footer


class Vector2D(Vector):
    __slots__ = ()
    NAMES = ('x', 'y')


    # Using Py3 keyword only syntax for dtype
    def __new__(cls, x=0, y=0, dtype=np.double):
        return Vector.__new__(cls, x, y, dtype=dtype)

    def phi(self):
        return np.arctan2(self.y, self.x).view(np.ndarray)

    def rho(self):
        return self[:2].view(Vector2D).mag().view(np.ndarray)

    def angle(self, other):
        'Angle between two vectors'
        return super(Vector2D, self).angle(other)

    def pt2(self):
        'Tranverse compenent squared'
        return self[:2].view(Vector2D).mag2().view(np.ndarray)

    def pt(self):
        'Tranverse compenent'
        return self.rho()

class Vector3D(Vector2D):
    __slots__ = ()
    NAMES = ('x', 'y', 'z')

    def __new__(cls, x=0, y=0, z=0, dtype=np.double):
        return Vector.__new__(cls, x, y, z, dtype=dtype)

    def cross(self, other):
        return Vector3D(self.y*other.z - self.z*other.y,
                        self.z*other.x - self.x*other.z,
                        self.x*other.y - self.y*other.x)

    def theta(self):
        prep = np.sqrt(self.x*self.x + self.y*self.y)
        return np.arctan2(prep,self.z).view(np.ndarray)

    def r(self):
        return self[:3].view(Vector3D).mag().view(np.ndarray)


    def in_basis(self, xhat, yhat, zhat):
        '''Must be unit vectors, should be orthogonal'''
        return Vector3D(self.dot(xhat),
                        self.dot(yhat),
                        self.dot(zhat))

    angle = Vector.angle

    def rotate_axis(self, axis, angle):
        """Rotate vector by a given angle (in radians) around a given axis."""
        u = axis.unit()

        c, s = np.cos(angle), np.sin(angle)
        c1 = 1. - c

        return self.__class__(
            (c + u.x ** 2 * c1) * self.x + (u.x * u.y * c1 - u.z * s) * self.y \
             + (u.x * u.z * c1 + u.y * s) * self.z,
            (u.x * u.y * c1 + u.z * s) * self.x + (c + u.y ** 2 * c1) * self.y \
             + (u.y * u.z * c1 - u.x * s) * self.z,
            (u.x * u.z * c1 - u.y * s) * self.x + (u.y * u.z * c1 + u.x * s) * self.y \
             + (c + u.z ** 2 * c1) * self.z
        )

    def rotate_euler(self, phi=0, theta=0, psi=0):
        # Rotate Z (phi)
        c1 = np.cos(phi)
        s1 = np.sin(phi)
        c2 = np.cos(theta)
        s2 = np.sin(theta)
        c3 = np.cos(psi)
        s3 = np.sin(psi)
        # Rotate Y (theta)
        fzx2 =-s2*c1
        fzy2 = s2*s1
        fzz2 = c2
        # Rotate Z (psi)
        fxx3 = c3*c2*c1 - s3*s1
        fxy3 =-c3*c2*s1 - s3*c1
        fxz3 = c3*s2
        fyx3 = s3*c2*c1 + c3*s1
        fyy3 =-s3*c2*s1 + c3*c1
        fyz3 = s3*s2
        # Transform v
        return self.__class__(
            fxx3*self.x + fxy3*self.y + fxz3*self.z,
            fyx3*self.x + fyy3*self.y + fyz3*self.z,
            fzx2*self.x + fzy2*self.y + fzz2*self.z)


    @classmethod
    def from_spherical_coords(cls, r, theta, phi):
        """Constructor from a space point specified in spherical coordinates.
        Parameters
        ----------
        r     : radius, the radial distance from the origin (r > 0)
        theta : inclination in radians (theta in [0, pi] rad)
        phi   : azimuthal angle in radians (phi in [0, 2pi) rad)
        """

        return cls(r * np.sin(theta) * np.cos(phi), r * np.sin(theta) * np.sin(phi), r * np.cos(theta))

    @classmethod
    def from_cylindrical_coords(cls, rho, phi, z):
        """Constructor from a space point specified in cylindrical coordinates.
        Parameters
        ----------
        rho : radial distance from the z-axis (rho > 0)
        phi : azimuthal angle in radians (phi in [-pi, pi) rad)
        z   : height
        """

        return cls(np.cos(phi) * rho, np.sin(phi) * rho, z)


class LorentzVector(Vector3D):
    NAMES = ('x', 'y', 'z', 't')
    METRIC = np.array([-1,-1,-1,1])
    __slots__ = ()

    def __new__(cls, x=0, y=0, z=0, t=0, dtype=np.double):
        return Vector.__new__(cls, x, y, z, t, dtype=dtype)

    @property
    def vect(self):
        return self[:3].view(Vector3D)
    @vect.setter
    def vect(self, obj):
        self[:3] = obj

    def p(self):
        '''
        >>> v = LorentzVector(1,2,3,.5)
        >>> v.p()
        array([ 3.74165739])
        '''
        return np.sqrt(self.vect.mag2())

    def e(self):
        '''
        >>> v = LorentzVector(1,2,3,.5)
        >>> v.e()
        array([ 5.26782688])
        '''
        return self.t

    def gamma(self):
        '''
        >>> v = LorentzVector(1,2,3,.5)
        >>> v.gamma()
        array([ 2.01818182])
        '''

        return 1/(1 - self.beta()**2)

    def beta(self):
        '''
        >>> v = LorentzVector(1,2,3,.5)
        >>> v.beta()
        array([ 0.71028481])
        '''
        return self.p() / self.e()

    def boost_vector(self):
        '''
        >>> v = LorentzVector(-0.212, 0.0327, 0.0327, -0.099)
        >>> v.BoostVector()
        Vector3D([[ 2.14141414],
               [-0.33030303],
               [-0.33030303]])
        >>> v = LorentzVector(1,2,3,4)
        >>> v.BoostVector()
        Vector3D([[ 0.25],
               [ 0.5 ],
               [ 0.75]])
        '''

        return (self[:3] / self[3]).view(Vector3D)

    def boost(self, vector3, inplace=False):
        '''
        >>> v = LorentzVector(1,2,3,.5)
        >>> bv = Vector3D(.1,.2,.3)
        >>> v.Boost(bv)
        LorentzVector([[ 1.13224412],
               [ 2.26448824],
               [ 3.39673236],
               [ 2.04882269]])
        '''

        b2 = vector3.mag2()
        gamma = 1.0 / np.sqrt(1-b2)
        gamma2 = (gamma - 1) / b2
        bp = self.vect.dot(vector3)
        if inplace:
            self.vect += gamma2*bp*vector3 + gamma*vector3*self.t
            self.t += bp
            self.t *= gamma
        else:
            v = self.vect + gamma2*bp*vector3 + gamma*vector3*self.t
            return self.__class__(v[0], v[1], v[2], gamma*(self.t+bp))

_add_names(Vector2D)
_add_names(Vector3D)
_add_names(LorentzVector)

@overload(Vector2D)
def Vector2D_t(*args, **kargs):
    return np.array
@overload(Vector3D)
def Vector3D_t(*args, **kargs):
    return np.array
@overload(LorentzVector)
def LorentzVector_t(*args, **kargs):
    return np.array

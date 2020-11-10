#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.math.vectors module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest
from pytest import approx
from functools import partial
import numpy as np
assert_allclose = partial(np.testing.assert_allclose, atol=.0000001)

from skhep.math.vectors import *
from skhep.utils.py23 import *
from skhep.utils.exceptions import *
from math import pi, sqrt


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
# From iterable removed (Use python * syntax instead)

def test_from_iterable():
    iterable = [1,2,3]
    vec = Vector3D(*iterable)
    assert np.all(vec == Vector3D(1,2,3))

    with pytest.raises(TypeError):
        iterable = [1, 2, 3, 4]
        Vector3D(*iterable)

def test_default_const_iterable():
    several_vec = Vector3D(1,2,[3,4,5])
    assert several_vec.shape == (3,3)

    several_vec = Vector3D([1,2,3],[2,3,4],[3,4,5])
    assert several_vec.shape == (3,3)

    with pytest.raises(ValueError):
        Vector3D([1, 2, 3], [2, 3], [3, 4, 5])

def test_vectors_3D_constructors():
    v1 = Vector3D()
    assert str(v1) == str(np.array([0.,0.,0.]))
    assert repr(v1) == "Vector3D([0., 0., 0.])"
    assert str(v1) == str(Vector3D.origin())

    v2 = Vector3D(1.,1.,1.)
    assert str(v2) == str(np.array([1.,1.,1.]))

    v3 = Vector3D.from_vector(v1)
    assert str(v3) == str(np.array([0.,0.,0.]))

    v4 = Vector3D(*[1.0, 1.0, 1.0])
    assert str(v4) == str(np.array([1.,1.,1.]))

    v5 = Vector3D.from_cylindrical_coords(1., 0., 1.)
    assert np.all(v5 == Vector3D(1., 0., 1.))
    assert v5.rho() == 1.

    v6 = Vector3D.from_cylindrical_coords(0.5, pi / 2, 0.)
    assert_allclose(v6, Vector3D(0., 0.5, 0.))

    v7 = Vector3D.from_spherical_coords(1.0, 0., 0.)
    assert np.all(v7 == Vector3D(0., 0., 1.))
    assert v7.r() == 1.
    assert v7.theta() == 0.

    v8 = Vector3D.from_spherical_coords(1.0, 0., pi / 2)
    assert_allclose(v8, Vector3D(0., 0., 1.))

    v9 = Vector3D.from_spherical_coords(2.0, pi / 2, pi / 4)
    assert_allclose(v9, Vector3D(sqrt(2), sqrt(2), 0.))

def test_vectors_Lorentz_constructors():
    with pytest.raises(ValueError):
        LorentzVector(*['str1', 'str2', 'str3', 'str4'])
    #
    lv1 = LorentzVector()
    assert str(lv1) == str(np.array([0.,0.,0.,0.]))
    assert repr(lv1) == "LorentzVector([0., 0., 0., 0.])"
    lv2 = LorentzVector(1., 1., 1., 1.)
    assert str(lv2) == str(np.array([1.,1.,1.,1.]))


def test_containers_properties():
    with pytest.raises(IndexError):
        Vector3D.__setitem__(Vector3D(), 3, 1.)
    with pytest.raises(IndexError):
        Vector3D.__getitem__(Vector3D(), 3)
    #
    v1 = Vector3D()
    v1.x = 5.; v1.y = -5.; v1.z = 10
    assert np.all(v1 == Vector3D(5., -5.,  10.))
    v1[:] = (-5., 5., 10.)
    assert np.all(v1 == Vector3D(-5., 5.,  10.))
    v1[0] = 1.
    assert np.all(v1 == Vector3D(1., 5.,  10.))
    v1[1] = 1.
    assert np.all(v1 == Vector3D(1., 1.,  10.))
    v1[2] = 1.
    assert np.all(v1 == Vector3D(1., 1.,  1.))
    assert v1[0] == 1.
    assert v1[1] == 1.
    assert v1[2] == 1.
    assert len(v1) == 3.
    assert v1.tolist() == [1., 1.,  1.]
    assert list(v1) == [1., 1.,  1.]
    assert [v for v in v1] == [1., 1.,  1.]
    #
    with pytest.raises(IndexError):
        LorentzVector.__setitem__(LorentzVector(), 4, 1.)
    with pytest.raises(IndexError):
        LorentzVector.__getitem__(LorentzVector(), 4)
    #
    lv1 = LorentzVector()
    lv1.x = 5.; lv1.y = -5.; lv1.z = 10; lv1.t = 2.
    assert np.all(lv1 == LorentzVector(5., -5., 10.,  2.))
    lv1.x = 5.; lv1.y = 5.; lv1.z = -10; lv1.t = 2.
    assert np.all(lv1 == LorentzVector(5., 5., -10.,  2.))
    lv1[:] = (-5., 5., 10., -2.)
    assert np.all(lv1 == LorentzVector(-5., 5., 10.,  -2.))
    lv1[0] = 1.
    assert np.all(lv1 == LorentzVector(1., 5., 10.,  -2.))
    lv1[1] = 1.
    assert np.all(lv1 == LorentzVector(1., 1., 10.,  -2.))
    lv1[2] = 1.
    assert np.all(lv1 == LorentzVector(1., 1., 1.,  -2.))
    lv1[3] = 1.
    assert np.all(lv1 == LorentzVector(1., 1., 1.,  1.))
    assert lv1[0] == 1.
    assert lv1[1] == 1.
    assert lv1[2] == 1.
    assert lv1[3] == 1.
    assert len(lv1) == 4.
    assert list(lv1) == [1., 1., 1.,  1.]

def test_vectors_3D_operators():

    v1 = Vector3D(0., 0., 0.)
    v2 = Vector3D(1., 1., 1.)
    v3 = Vector3D(2., 2., 2.)
    v4 = Vector3D(3., 3., 3.)
    v5 = Vector3D(1., 2., 3.)

    assert np.all(v1 == 0.)
    assert_allclose(v1 + v2, Vector3D(1., 1., 1.))
    assert_allclose(v1 - v2, Vector3D(-1., -1., -1.))
    assert_allclose(v1 - v2, -1.*Vector3D(1., 1., 1.))
    assert_allclose(v1 * 2., Vector3D(0., 0., 0.))
    assert_allclose(v2 * 2., Vector3D(2., 2., 2.))
    assert_allclose(2. * v1, Vector3D(0., 0.,  0.))
    assert_allclose(2. * v2, Vector3D(2., 2., 2.))

    assert v1.dot(v2) == 0.
    assert v2.dot(v1) == 0.
    assert v4.dot(v3) == v3.dot(v4)
    assert v3.dot(v4) == 18.
    assert_allclose( v3 / 2. , v2)
    assert_allclose( v4 / 3. , v2)
    v1 *= 2.
    v2 *= 2.
    assert np.all(v1 == Vector3D(0., 0., 0.))
    assert np.all(v2 == Vector3D(2., 2., 2.))
    v1 /= 2.
    v2 /= 2.
    assert np.all(v1 == Vector3D(0., 0., 0.))
    assert np.all(v2 == Vector3D(1., 1., 1.))
    assert (v1 + v2).dot(v3) == 6., "Check operations combination"
    assert (v2 - v1).dot(v3) == 6., "Check operations combination"
    assert v3.dot((v1 - v2)) == -6., "Check operations combination"
    assert 18. / (v3.dot(v4)) == 1., "Check operations combination"
    assert_allclose(v4 / (v3.dot(v2)) , Vector3D(0.5, 0.5, 0.5))
    assert_allclose( v2.cross(v2), Vector3D(0., 0., 0.))
    assert_allclose( v2.cross(v5), Vector3D(1., -2., 1.))
    assert_allclose( v5.cross(v2), -1 * v2.cross(v5))
    assert_allclose( v2, v2)

def test_vectors_Lorentz_operators():
    with pytest.raises(TypeError):
        LorentzVector.__iadd__(LorentzVector(), "a")
    with pytest.raises(TypeError):
        LorentzVector.__isub__(LorentzVector(), "a")
    #
    lv1 = LorentzVector(0., 0., 0., 0.)
    lv2 = LorentzVector(1., 1., 1., 0.)
    lv3 = LorentzVector(2., 2., 2., 1.)
    lv4 = LorentzVector(3., 3., 3., 1.)
    lv5 = LorentzVector(1., 1., 1., 6.)
    assert np.all(lv1 == 0.)
    assert_allclose( lv1 + lv2 , LorentzVector(1., 1., 1.,  0.))
    assert_allclose( lv1 - lv2 , LorentzVector(-1., -1., -1.,  0.))
    assert_allclose( lv1 * 2. , LorentzVector(0., 0., 0.,  0.))
    assert_allclose( lv2 * 2. , LorentzVector(2., 2., 2.,  0.))
    assert_allclose( 2. * lv1 , LorentzVector(0., 0., 0.,  0.))
    assert_allclose( 2. * lv2 , LorentzVector(2., 2., 2.,  0.))
    assert lv2.dot(lv1) == 0.
    assert lv1.dot(lv2) == 0.
    assert lv3.dot(lv4) == lv4.dot(lv3)
    assert lv3.dot(lv4) == -17.
    assert_allclose( lv3 / 2. , LorentzVector(1., 1., 1.,  0.5))
    assert_allclose( lv4 / 3. , LorentzVector(1., 1., 1.,  1./3))
    assert lv3.dot(lv5) == 0.0
    lv1 *= 2.
    lv2 *= 2.
    assert_allclose( lv1 , LorentzVector(0., 0., 0.,  0.))
    assert_allclose( lv2 , LorentzVector(2., 2., 2.,  0.))
    lv1 /= 2.
    lv2 /= 2.

    assert_allclose( lv1 , LorentzVector(0., 0., 0.,  0.))
    assert_allclose( lv2 , LorentzVector(1., 1., 1.,  0.))
    assert_allclose( lv2 , lv2)


def test_vectors_3D_rotations():
    v1 = Vector3D.from_cylindrical_coords(1., 0., 0.)
    assert v1.phi() == 0.0
    assert v1.rotate_axis(Vector3D.Z, pi/2).phi() == pi/2
    assert_allclose(v1.rotate_axis(Vector3D.Z, pi/2), Vector3D(0., 1.,  0.), atol = .0000001)
    assert v1.rotate_axis(Vector3D.Y, pi).phi() == pi
    assert v1.rotate_axis(Vector3D.Y, -pi).phi() == pi
    assert_allclose( v1.rotate_axis(Vector3D.Y, pi) , Vector3D(-1., 0.,  0.), atol = .0000001)
    assert_allclose( v1.rotate_axis(Vector3D.Y, -pi) , Vector3D(-1., 0.,  0.), atol = .0000001)
    assert v1.rotate_axis(Vector3D.X, pi).phi() == 0.
    assert_allclose(v1.rotate_axis(Vector3D.X, pi) , Vector3D(1., 0.,  0.), atol = .0000001)
    v2 = Vector3D.from_spherical_coords(1.0, pi / 2, pi / 2)
    assert v2.phi() == pi/2
    assert v2.theta() == pi/2
    assert v2.rotate_axis(Vector3D.X, pi).phi() == -pi/2
    assert v2.rotate_axis(Vector3D.X, pi).theta() == pi/2
    assert_allclose(v2.rotate_axis(Vector3D.X, pi), Vector3D(0., -1.,  0.), atol = .0000001)
    v3 = Vector3D.from_spherical_coords(1.0, pi / 4, pi / 4)
    angle = v2.angle(v3)
    axis = v2.cross(v3)
    assert_allclose( v2.rotate_axis(axis, angle) ,  v3, atol = .0000001)
    assert_allclose( v2.rotate_axis(-1.*axis, -angle) ,  v3, atol = .0000001)

def test_vectors_Lorentz_rotations():
    v1 = Vector3D.from_cylindrical_coords(1., 0., 0.)
    v2 = Vector3D.from_spherical_coords(1.0, pi / 2, pi / 2)
    v3 = Vector3D.from_spherical_coords(1.0, pi / 4, pi / 4)
    angle = v2.angle(v3)
    axis = v2.cross(v3)

    with pytest.raises(AttributeError):
        LorentzVector.rotate_axis(LorentzVector(), pi, 1)
    with pytest.raises(AttributeError):
        LorentzVector.rotate_axis(LorentzVector(), pi, [1,2])
    with pytest.raises(TypeError):
        LorentzVector.rotate_axis(LorentzVector(), pi, 1, 2, 3, 4)
    with pytest.raises(TypeError):
        LorentzVector.rotate_axis(LorentzVector(), pi, 0, 1, 'a')
    with pytest.raises(AttributeError):
        LorentzVector.rotate_axis(LorentzVector(), pi, ['a','b',3])
    #
    lv1 = LorentzVector(*v1, 1.)
    assert lv1.phi() == 0.
    assert lv1.rotate_axis(Vector3D.Z, pi/2).phi() == pi/2
    assert_allclose( lv1.rotate_axis(Vector3D.Z,pi/2) , LorentzVector(0., 1., 0.,  1.))
    assert lv1.rotate_axis(Vector3D.Y,pi).phi() == pi
    assert lv1.rotate_axis(Vector3D.Y,-pi).phi() == pi
    assert_allclose( lv1.rotate_axis(Vector3D.Y,pi) , LorentzVector(-1., 0., 0.,  1.))
    assert_allclose( lv1.rotate_axis(Vector3D.Y,-pi) , LorentzVector(-1., 0., 0.,  1.))
    assert lv1.rotate_axis(Vector3D.X,pi).phi() == 0.
    assert_allclose( lv1.rotate_axis(Vector3D.X,pi) , LorentzVector(1., 0., 0.,  1.))
    lv2 = LorentzVector(*v2, 2.0)
    assert lv2.phi() == pi/2
    assert lv2.theta() == pi/2
    assert lv2.rotate_axis(Vector3D.X,pi).phi() == -pi/2
    assert lv2.rotate_axis(Vector3D.X,pi).theta() == pi/2
    assert_allclose( lv2.rotate_axis(Vector3D.X,pi) , LorentzVector(0., -1., 0.,  2.0))
    lv3 = LorentzVector(*v3, 2.0)
    assert_allclose( lv2.rotate_axis(axis, angle) ,  lv3, atol = .0000001)
    assert_allclose( lv2.rotate_axis(-1.*axis, -angle) , lv3, atol = .0000001)

def test_3Dvectors_properties():
    v0 = Vector3D()
    v1, v2 = Vector3D(1., 1., 1.), Vector3D(2., 2., 2.)
    v3, v4 = Vector3D(-1., -1., -1.), Vector3D(-2., -2., -2.)
    v5, v6 = Vector3D(1., 1., 0.), Vector3D(0., 0., 2.)
    assert np.all(v0 == [0,0,0])
    assert np.all(v1 == [1,1,1])
    assert v1.mag2() == 3.
    assert v1.mag() == sqrt(3.)
    assert v2.mag2() == 12.
    assert v2.mag() == sqrt(12.)
    assert v1.unit().mag() == 1.
    v7 = v1.unit()
    assert np.all(v1.unit() == v7.unit())

    # assert v1.isparallel(v2) == True
    # assert v2.isparallel(v1) == True
    # assert v1.isantiparallel(v2) == False
    # assert v2.isantiparallel(v1) == False
    # assert v1.isantiparallel(v3) == True
    # assert v2.isantiparallel(v4) == True
    # assert v1.isparallel(v3) == False
    # assert v2.isparallel(v4) == False
    # assert v1.isopposite(v3) == True
    # assert v1.isopposite(v4) == False
    # assert v2.isopposite(v4) == True
    # assert v2.isopposite(v3) == False
    # assert v1.isperpendicular(v2) == False
    # assert v2.isperpendicular(v1) == False
    # assert v5.isperpendicular(v6) == True
    # assert v6.isperpendicular(v5) == True

def test_lorentz_vectors_errors():
    with pytest.raises(AttributeError):
        LorentzVector.boost(LorentzVector(), 1)
    with pytest.raises(AttributeError):
        LorentzVector.boost(LorentzVector(), [1,2])
    with pytest.raises(TypeError):
        LorentzVector.boost(LorentzVector(), 1, 2, 3, 4)
    with pytest.raises(TypeError):
        LorentzVector.boost(LorentzVector(), 0, 1, 'a')
    with pytest.raises(AttributeError):
        LorentzVector.boost(LorentzVector(), ['a','b',3])

def test_lorentz_vectors_properties():
    lv0 = LorentzVector()
    lv1 = LorentzVector(1., 1., 1., 1.)
    lv2 = LorentzVector(1., 1., 1., 2.)
    assert np.all(lv1.boost_vector() == Vector3D(1., 1.,  1.))
    assert lv1.p() == np.sqrt(3.)
    assert lv1.e() == 1.
    assert lv1.beta() == sqrt(3.)
    assert np.all(lv2.boost_vector() == Vector3D(0.5, 0.5,  0.5))
    lv3 = LorentzVector(0., 0., 1., 0.)
    beta = 0.05
    gamma = 1/sqrt(1 - beta**2)
    lv4 = lv3.boost(Vector3D(0,0,beta))
    assert lv4.z == lv3.z * gamma,  "Check length contraction"
    assert lv4.x == lv3.x
    assert lv4.y == lv3.x
    assert lv4.t == - gamma * (lv3.t - beta * lv3.z) # Added -
    assert_allclose(lv4, LorentzVector(lv3.x, lv3.y, lv3.z * gamma, -gamma * (lv3.t - beta * lv3.z))) # Added -
    lv5 = LorentzVector(0., 0., 0., 1.)
    assert lv5.beta() == 0.
    assert lv5.gamma() == 1.
    assert_allclose(lv5.boost(Vector3D(0,0,0)), lv5)
    lv6 = lv5.boost(Vector3D(0,beta,0))
    assert lv6.x == lv5.x
    assert lv6.z == lv5.z
    assert lv6.t == lv5.t * gamma,  "Check time dilation"
    assert lv6.y == -gamma * (lv5.y - beta*lv5.t)
    assert_allclose(lv6 , LorentzVector(lv5.x, -gamma * (lv5.y - beta*lv5.t), lv5.z,  lv5.t * gamma))


def test_lorentz_vectors_properties_again():
    p1 = LorentzVector(5.,5.,10.,5)
    assert p1.x == 5.
    assert p1.y == 5.
    assert p1.z == 10.
    assert p1.t == 5.
    assert p1.mag() == approx(-11.180340)
    assert p1.mag2() == approx(-125)
    assert p1.pt() == sqrt(p1.x**2 + p1.y**2)
    assert p1.p() == sqrt(p1.x**2 + p1.y**2 + p1.z**2)
    assert p1.p() == sqrt(p1.pt()**2 + p1.z**2)
    assert p1.e() == sqrt(p1.mag2() + p1.p()**2)
    assert p1.beta() == p1.p() / p1.e()

def test_lorentz_vectors_boosting():
    p3 = LorentzVector(5.,5.,10.,20)
    assert p3.x == 5.
    assert p3.y == 5.
    assert p3.z == 10.
    assert p3.e() == 20.
    assert p3.mag() == sqrt(p3.e()**2 - p3.p()**2)
    assert p3.beta() == p3.p() / p3.e()

    p4 = LorentzVector.from_pt_eta_phi_m(10., 3.5, pi/3, 5.)
    assert p4.pt() == approx(10.)
    assert p4.eta() == approx(3.5)
    assert p4.phi() == approx(pi/3)
    assert p4.mag() == approx(5.)

    p5 = LorentzVector.from_pt_eta_phi(10., 3.9, -2*(pi/3), 20.)
    assert p5.pt() == approx(10.)
    assert p5.eta() == approx(3.9)
    assert p5.phi() == approx(-2*(pi/3))
    assert p5.e() == approx(20.)
    assert p5.eta() - p4.eta() == approx(0.4)
    assert p5.phi() - p4.phi() == approx(-pi)
    assert p5.delta_r(p4) == approx(sqrt(0.4**2 + pi**2))

    p6 = LorentzVector.from_pt_eta_phi(10.,3.9,-pi,20.)
    assert np.mod(p6.phi() - p4.phi() + np.pi, np.pi*2) - np.pi == approx(2*(pi/3))
    assert np.mod(p4.phi() - p6.phi() + np.pi, np.pi*2) - np.pi == approx(-2*(pi/3))

    p7 = LorentzVector(5.,5.,5.,0.)
    assert p7.beta() == np.inf
    assert np.isnan(p7.gamma()),  "Gamma of the photons is +inf"
    # assert p7.p() == p7.e(),  "Momentum = Energy for photons"
    assert np.isnan(p7.rapidity())

    p8 = LorentzVector.from_pt_eta_phi(10.,2E2,-2*(pi/3),20.) #sinh(eta) diverge quickly
    assert p8.theta() == approx(0.0)
    assert p8.eta() > 1E10



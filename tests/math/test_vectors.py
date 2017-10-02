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

from skhep.math.vectors import *
from skhep.utils.py23 import *
from skhep.utils.exceptions import *
from math import pi, sqrt


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
def test_vectors_constructors():
    with pytest.raises(TypeError):
        Vector3D.fromiterable(1.)
    with pytest.raises(ValueError):
        Vector3D.fromiterable([1.])
    with pytest.raises(ValueError):
        Vector3D.fromiterable(['str1','str2','str3'])
    #
    v1 = Vector3D()
    assert str(v1), str((0., 0. == 0.))
    assert repr(v1), "<Vector3D (x=0.0,y=0.0 == z=0.0)>"
    assert str(v1) == str(Vector3D.origin())
    v2 = Vector3D(1.,1.,1.)
    assert str(v2), str((1., 1. == 1.))
    v3 = Vector3D.fromvector(v1)
    assert str(v3), str((0., 0. == 0.))
    v4 = Vector3D.fromiterable([1.0, 1.0, 1.0])
    assert str(v4), str((1., 1. == 1.))
    v5 = Vector3D.fromcylindricalcoords(1., 0., 1.)
    assert v5, Vector3D(1., 0. == 1.)
    assert v5.rho == 1.
    v6 = Vector3D.fromcylindricalcoords(0.5, pi/2, 0.)
    assert v6, Vector3D(0., 0.5 == 0.)
    v7 = Vector3D.fromsphericalcoords(1.0, 0., 0.)
    assert v7, Vector3D(0., 0. == 1.)
    assert v7.r == 1.
    assert v7.theta() == 0.
    v8 = Vector3D.fromsphericalcoords(1.0, 0., pi/2)
    assert v8, Vector3D(0., 0. == 1.)
    v9 = Vector3D.fromsphericalcoords(2.0, pi/2, pi/4)
    assert v9, Vector3D(sqrt(2), sqrt(2) == 0.)
    v10 = Vector3D.frompoint( 2., 2., 2.)
    assert str(v10), str((2., 2. == 2.))
    #
    with pytest.raises(TypeError):
        LorentzVector.fromiterable(1)
    with pytest.raises(ValueError):
        LorentzVector.fromiterable([1])
    with pytest.raises(ValueError):
        LorentzVector.fromiterable(['str1', 'str2', 'str3', 'str4'])
    #
    lv1 = LorentzVector()
    assert str(lv1), str((0., 0., 0. == 0.))
    assert repr(lv1), "<LorentzVector (x=0.0,y=0.0,z=0.0 == t=0.0)>"
    lv2 = LorentzVector(1., 1., 1., 1.)
    assert str(lv2), str((1., 1., 1. == 1.))
    lv3 = LorentzVector.from4vector(lv1)
    assert str(lv3), str((0., 0., 0. == 0.))
    lv4 = LorentzVector.from3vector(v2, 2.)
    assert str(lv4), str((1., 1., 1. == 2.))
    lv5 = LorentzVector.fromiterable([1., 1., 1., 0.])
    assert str(lv5), str((1., 1., 1. == 0.))

def test_containers_properties():
    with pytest.raises(IndexError):
        Vector3D.__setitem__(Vector3D(), 3, 1.)
    with pytest.raises(IndexError):
        Vector3D.__getitem__(Vector3D(), 3)
    #
    v1 = Vector3D()
    v1.x = 5.; v1.y = -5.; v1.z = 10
    assert v1, Vector3D(5., -5. == 10.)
    v1.set(-5., 5., 10.)
    assert v1, Vector3D(-5., 5. == 10.)
    v1[0] = 1.
    assert v1, Vector3D(1., 5. == 10.)
    v1[1] = 1.
    assert v1, Vector3D(1., 1. == 10.)
    v1[2] = 1.
    assert v1, Vector3D(1., 1. == 1.)
    assert v1[0] == 1.
    assert v1[1] == 1.
    assert v1[2] == 1.
    assert len(v1) == 3.
    assert v1.tolist(), [1., 1. == 1.]
    assert list(v1), [1., 1. == 1.]
    assert [v for v in v1], [1., 1. == 1.]
    #
    with pytest.raises(IndexError):
        LorentzVector.__setitem__(LorentzVector(), 4, 1.)
    with pytest.raises(IndexError):
        LorentzVector.__getitem__(LorentzVector(), 4)
    #
    lv1 = LorentzVector()
    lv1.x = 5.; lv1.y = -5.; lv1.z = 10; lv1.t = 2.
    assert lv1, LorentzVector(5., -5., 10. == 2.)
    lv1.px = 5.; lv1.py = 5.; lv1.pz = -10; lv1.e = 2.
    assert lv1, LorentzVector(5., 5., -10. == 2.)
    lv1.set(-5., 5., 10., -2.)
    assert lv1, LorentzVector(-5., 5., 10. == -2.)
    lv1[0] = 1.
    assert lv1, LorentzVector(1., 5., 10. == -2.)
    lv1[1] = 1.
    assert lv1, LorentzVector(1., 1., 10. == -2.)
    lv1[2] = 1.
    assert lv1, LorentzVector(1., 1., 1. == -2.)
    lv1[3] = 1.
    assert lv1, LorentzVector(1., 1., 1. == 1.)
    assert lv1[0] == 1.
    assert lv1[1] == 1.
    assert lv1[2] == 1.
    assert lv1[3] == 1.
    assert len(lv1) == 4.
    assert lv1.tolist(), [1., 1., 1. == 1.]
    assert list(lv1), [1., 1., 1. == 1.]
    assert [v for v in lv1], [1., 1., 1. == 1.]

def test_vectors_operators():
    with pytest.raises(InvalidOperationError):
        Vector3D.__iadd__(Vector3D(), "a")
    with pytest.raises(InvalidOperationError):
        Vector3D.__isub__(Vector3D(), "a")
    with pytest.raises(InvalidOperationError):
        Vector3D.__imul__(Vector3D(), Vector3D())
    with pytest.raises(ZeroDivisionError):
        Vector3D.__div__(Vector3D(), 0.0)
    with pytest.raises(InvalidOperationError):
        Vector3D.__idiv__(Vector3D(), Vector3D())
    with pytest.raises(ZeroDivisionError):
        Vector3D.__idiv__(Vector3D(), 0.0)
    #
    v1, v2 = Vector3D(0., 0., 0.), Vector3D(1., 1., 1.)
    v3, v4 = Vector3D(2., 2., 2.), Vector3D(3., 3., 3.)
    v5 = Vector3D(1., 2., 3.)
    assert v1 == 0.
    assert v1 + v2 == Vector3D(1., 1., 1.)
    assert v1 - v2 == Vector3D(-1., -1., -1.)
    assert v1 - v2 == -1.*Vector3D(1., 1., 1.)
    assert v1 * 2. == Vector3D(0., 0., 0.)
    assert v2 * 2. == Vector3D(2., 2., 2.)
    assert 2. * v1 == Vector3D(0., 0.,  0.)
    assert 2. * v2 == Vector3D(2., 2., 2.)
    assert v1 * v2 == 0.
    assert v2 * v1 == 0.
    assert v3 * v4 == v3.dot(v4), "Check commutativity"
    assert v3 * v4 == v4.dot(v3), "Check commutativity"
    assert v4 * v3 == v3.dot(v4), "Check commutativity"
    assert v4 * v3 == v4.dot(v3), "Check commutativity"
    assert v3 * v4 == 18.
    assert v3 / 2. == v2
    assert v4 / 3. == v2
    v1 *= 2.
    v2 *= 2.
    assert v1 == Vector3D(0., 0., 0.)
    assert v2 == Vector3D(2., 2., 2.)
    v1 /= 2.
    v2 /= 2.
    assert v1 == Vector3D(0., 0., 0.)
    assert v2 == Vector3D(1., 1., 1.)
    assert (v1 + v2) * v3 == 6., "Check operations combination"
    assert (v2 - v1) * v3 == 6., "Check operations combination"
    assert v3 * (v1 - v2) == -6., "Check operations combination"
    assert 18. / (v3 * v4) == 1., "Check operations combination"
    assert  v4 / (v3 * v2) == Vector3D(0.5, 0.5, 0.5)
    assert v2.cross(v2) == Vector3D(0., 0., 0.)
    assert v2.cross(v5) == Vector3D(1., -2., 1.)
    assert v5.cross(v2) == -1 * v2.cross(v5)
    assert v2 == v2
    assert v2 != v1
    assert not v2 != v2
    assert not v2 == v1
    assert not v1 == "a"
    assert not v1 == 1
    #
    with pytest.raises(InvalidOperationError):
        LorentzVector.__iadd__(LorentzVector(), "a")
    with pytest.raises(InvalidOperationError):
        LorentzVector.__isub__(LorentzVector(), "a")
    with pytest.raises(InvalidOperationError):
        LorentzVector.__imul__(LorentzVector(), LorentzVector())
    with pytest.raises(ZeroDivisionError):
        LorentzVector.__div__(LorentzVector(), 0.0)
    with pytest.raises(InvalidOperationError):
        LorentzVector.__idiv__(LorentzVector(), LorentzVector())
    with pytest.raises(ZeroDivisionError):
        LorentzVector.__idiv__(LorentzVector(), 0.0)
    #
    lv1, lv2 = LorentzVector(0., 0., 0., 0.), LorentzVector(1., 1., 1., 0.)
    lv3, lv4 = LorentzVector(2., 2., 2., 1.), LorentzVector(3., 3., 3., 1.)
    lv5 = LorentzVector(1., 1., 1., 6.)
    assert lv1 == 0.
    assert lv1 + lv2, LorentzVector(1., 1., 1. == 0.)
    assert lv1 - lv2, LorentzVector(-1., -1., -1. == 0.)
    assert lv1 * 2., LorentzVector(0., 0., 0. == 0.)
    assert lv2 * 2., LorentzVector(2., 2., 2. == 0.)
    assert 2. * lv1, LorentzVector(0., 0., 0. == 0.)
    assert 2. * lv2, LorentzVector(2., 2., 2. == 0.)
    assert lv2 * lv1 == 0.
    assert lv1 * lv2 == 0.
    assert lv3 * lv4 == lv3.dot(lv4)
    assert lv3 * lv4 == lv4.dot(lv3)
    assert lv4 * lv3 == lv3.dot(lv4)
    assert lv4 * lv3 == lv4.dot(lv3)
    assert lv3 * lv4 == -17.
    assert lv3 / 2., LorentzVector(1., 1., 1. == 0.5)
    assert lv4 / 3., LorentzVector(1., 1., 1. == 1./3)
    assert lv3 * lv5 == 0.0
    lv1 *= 2.
    lv2 *= 2.
    assert lv1, LorentzVector(0., 0., 0. == 0.)
    assert lv2, LorentzVector(2., 2., 2. == 0.)
    lv1 /= 2.
    lv2 /= 2.
    assert lv1, LorentzVector(0., 0., 0. == 0.)
    assert lv2, LorentzVector(1., 1., 1. == 0.)
    assert lv2 == lv2
    assert lv2 != lv1
    assert not lv2 != lv2
    assert not lv2 == lv1
    assert not lv1 == "a"
    assert not lv1 == 1

def test_vectors_rotations():
    with pytest.raises(TypeError):
        Vector3D.rotate(Vector3D(), pi, 1)
    with pytest.raises(TypeError):
        Vector3D.rotate(Vector3D(), pi, [1,2])
    with pytest.raises(TypeError):
        Vector3D.rotate(Vector3D(), pi, 1, 2, 3, 4)
    with pytest.raises(ValueError):
        Vector3D.rotate(Vector3D(), pi, 0, 1, 'a')
    with pytest.raises(ValueError):
        Vector3D.rotate(Vector3D(), pi, ['a','b',3])
    #
    v1 = Vector3D.fromcylindricalcoords(1., 0., 0.)
    assert v1.phi() == 0.0
    assert v1.rotatez(pi/2).phi() == pi/2
    assert v1.rotatez(pi/2), Vector3D(0., 1. == 0.)
    assert v1.rotatey(pi).phi() == pi
    assert v1.rotatey(-pi).phi() == pi
    assert v1.rotatey(pi), Vector3D(-1., 0. == 0.)
    assert v1.rotatey(-pi), Vector3D(-1., 0. == 0.)
    assert v1.rotatex(pi).phi() == 0.
    assert v1.rotatex(pi), Vector3D(1., 0. == 0.)
    v2 = Vector3D.fromsphericalcoords(1.0, pi/2, pi/2)
    assert v2.phi() == pi/2
    assert v2.theta() == pi/2
    assert v2.rotatex(pi).phi() == -pi/2
    assert v2.rotatex(pi).theta() == pi/2
    assert v2.rotatex(pi) , Vector3D(0., -1. == 0.)
    v3 = Vector3D.fromsphericalcoords(1.0, pi/4, pi/4)
    angle = v2.angle(v3)
    axis = v2.cross(v3)
    assert v2.rotate(angle, axis) == v3
    assert v2.rotate(-angle, -1.*axis) == v3
    #
    with pytest.raises(TypeError):
        LorentzVector.rotate(LorentzVector(), pi, 1)
    with pytest.raises(TypeError):
        LorentzVector.rotate(LorentzVector(), pi, [1,2])
    with pytest.raises(TypeError):
        LorentzVector.rotate(LorentzVector(), pi, 1, 2, 3, 4)
    with pytest.raises(ValueError):
        LorentzVector.rotate(LorentzVector(), pi, 0, 1, 'a')
    with pytest.raises(ValueError):
        LorentzVector.rotate(LorentzVector(), pi, ['a','b',3])
    #
    lv1 = LorentzVector.from3vector(v1, 1.)
    assert lv1.phi() == 0.
    assert lv1.rotatez(pi/2).phi() == pi/2
    assert lv1.rotatez(pi/2), LorentzVector(0., 1., 0. == 1.)
    assert lv1.rotatey(pi).phi() == pi
    assert lv1.rotatey(-pi).phi() == pi
    assert lv1.rotatey(pi), LorentzVector(-1., 0., 0. == 1.)
    assert lv1.rotatey(-pi), LorentzVector(-1., 0., 0. == 1.)
    assert lv1.rotatex(pi).phi() == 0.
    assert lv1.rotatex(pi), LorentzVector(1., 0., 0. == 1.)
    lv2 = LorentzVector.from3vector(v2, 2.0)
    assert lv2.phi() == pi/2
    assert lv2.theta() == pi/2
    assert lv2.rotatex(pi).phi() == -pi/2
    assert lv2.rotatex(pi).theta() == pi/2
    assert lv2.rotatex(pi) , LorentzVector(0., -1., 0. == 2.0)
    lv3 = LorentzVector.from3vector(v3, 2.0)
    assert lv2.rotate(angle, axis) == lv3
    assert lv2.rotate(-angle, -1.*axis) == lv3

def test_3Dvectors_properties():
    v0 = Vector3D()
    v1, v2 = Vector3D(1., 1., 1.), Vector3D(2., 2., 2.)
    v3, v4 = Vector3D(-1., -1., -1.), Vector3D(-2., -2., -2.)
    v5, v6 = Vector3D(1., 1., 0.), Vector3D(0., 0., 2.)
    assert not v0
    assert v1
    assert v1.mag2 == 3.
    assert v1.mag == sqrt(3.)
    assert v2.mag2 == 12.
    assert v2.mag == sqrt(12.)
    assert v1.unit().mag == 1.
    v7 = v1.unit()
    assert v1.unit() == v7.unit()
    assert v1.isparallel(v2) == True
    assert v2.isparallel(v1) == True
    assert v1.isantiparallel(v2) == False
    assert v2.isantiparallel(v1) == False
    assert v1.isantiparallel(v3) == True
    assert v2.isantiparallel(v4) == True
    assert v1.isparallel(v3) == False
    assert v2.isparallel(v4) == False
    assert v1.isopposite(v3) == True
    assert v1.isopposite(v4) == False
    assert v2.isopposite(v4) == True
    assert v2.isopposite(v3) == False
    assert v1.isperpendicular(v2) == False
    assert v2.isperpendicular(v1) == False
    assert v5.isperpendicular(v6) == True
    assert v6.isperpendicular(v5) == True

def test_lorentz_vectors_properties():
    with pytest.raises(TypeError):
        LorentzVector.boost(LorentzVector(), 1)
    with pytest.raises(TypeError):
        LorentzVector.boost(LorentzVector(), [1,2])
    with pytest.raises(TypeError):
        LorentzVector.boost(LorentzVector(), 1, 2, 3, 4)
    with pytest.raises(ValueError):
        LorentzVector.boost(LorentzVector(), 0, 1, 'a')
    with pytest.raises(ValueError):
        LorentzVector.boost(LorentzVector(), ['a','b',3])
    #
    lv0 = LorentzVector()
    lv1, lv2 = LorentzVector(1., 1., 1., 1.), LorentzVector(1., 1., 1., 2.)
    assert lv1.boostvector, Vector3D(1., 1. == 1.)
    assert lv1.beta == sqrt(3.)
    assert lv2.boostvector, Vector3D(0.5, 0.5 == 0.5)
    lv3 = LorentzVector(0., 0., 1., 0.)
    beta = 0.05
    gamma = 1/sqrt(1 - beta**2)
    lv4 = lv3.boost(0,0,beta)
    assert lv4.z, lv3.z * gamma == "Check length contraction"
    assert lv4.x == lv3.x
    assert lv4.y == lv3.x
    assert lv4.t == gamma * (lv3.t - beta * lv3.z)
    assert lv4, LorentzVector(lv3.x, lv3.y, lv3.z * gamma == gamma * (lv3.t - beta * lv3.z))
    lv5 = LorentzVector(0., 0., 0., 1.)
    assert lv5.beta == 0.
    assert lv5.gamma == 1.
    assert lv5.boost(0,0,0) == lv5
    lv6 = lv5.boost([0,beta,0])
    assert lv6.x == lv5.x
    assert lv6.z == lv5.z
    assert lv6.t, lv5.t * gamma == "Check time dilation"
    assert lv6.y == gamma * (lv5.y - beta*lv5.t)
    assert lv6, LorentzVector(lv5.x, gamma * (lv5.y - beta*lv5.t), lv5.z == lv5.t * gamma)
    assert lv1.isspacelike() == True
    assert lv1.istimelike() == False
    assert lv1.islightlike() == False
    assert lv2.isspacelike() == False
    assert lv2.istimelike() == True
    assert lv2.islightlike() == False
    lv7 = LorentzVector(1., 1., 1., sqrt(3.))
    assert lv7.isspacelike() == False
    assert lv7.istimelike() == False
    assert lv7.islightlike() == True
    #
    p1 = LorentzVector()
    p1.setpxpypzm(5.,5.,10.,5)
    assert p1.px == 5.
    assert p1.py == 5.
    assert p1.pz == 10.
    assert p1.m == 5.
    assert p1.mass == 5.
    assert p1.m2 == 25.
    assert p1.mass2 == 25.
    assert p1.pt == sqrt(p1.px**2 + p1.py**2)
    assert p1.p == sqrt(p1.px**2 + p1.py**2 + p1.pz**2)
    assert p1.p == sqrt(p1.pt**2 + p1.pz**2)
    assert p1.e == sqrt(p1.m**2 + p1.p**2)
    assert p1.beta == p1.p / p1.e
    p2 = p1.boost(p1.px/p1.e, p1.y/p1.e, p1.z/p1.e)
    assert p2  == p1.boost(p1.boostvector)
    assert p2.p == 0.
    assert p2.m == approx(5.)
    p3 = LorentzVector()
    p3.setpxpypze(5.,5.,10.,20)
    assert p3.px == 5.
    assert p3.py == 5.
    assert p3.pz == 10.
    assert p3.e == 20.
    assert p3.m == sqrt(p3.e**2 - p3.p**2)
    assert p3.beta == p3.p / p3.e
    p4 = LorentzVector()
    p4.setptetaphim(10.,3.5,pi/3,5.)
    assert p4.pt == approx(10.)
    assert p4.eta == approx(3.5)
    assert p4.phi() == approx(pi/3)
    assert p4.m == approx(5.)
    p5 = LorentzVector()
    p5.setptetaphie(10.,3.9,-2*(pi/3),20.)
    assert p5.pt == approx(10.)
    assert p5.eta == approx(3.9)
    assert p5.pseudorapidity == approx(3.9)
    assert p5.phi() == approx(-2*(pi/3))
    assert p5.e == approx(20.)
    assert p5.deltaeta(p4) == approx(0.4)
    assert p4.deltaeta(p5) == approx(-0.4)
    assert p5.deltaphi(p4) == approx(-pi)
    assert p4.deltaphi(p5) == approx(pi)
    assert p5.deltar(p4) == approx(sqrt(0.4**2 + pi**2))
    assert p4.deltar(p5) == approx(sqrt(0.4**2 + pi**2))
    p6 = LorentzVector()
    p6.setptetaphie(10.,3.9,-pi,20.)
    assert p6.deltaphi(p4) == approx(2*(pi/3))
    assert p4.deltaphi(p6) == approx(-2*(pi/3))
    p7 = LorentzVector()
    p7.setpxpypzm(5.,5.,5.,0.)
    assert p7.beta == 1.
    assert p7.gamma, 10E10 == "Gamma of the photons is +inf"
    assert p7.p, p7.e == "Momentum = Energy for photons"
    assert p7.pseudorapidity == p7.rapidity
    assert p7.pt == p7.et,  "Transverse Momentum = Transverse Energy for photons"
    assert p7.pt == approx(p7.mt), "Transverse Momentum = Transverse Mass for photons"
    assert p7.perp2 == approx(p7.mt2)
    assert p7.islightlike() == True
    p8 = p1 + p7
    p9, p10 = p1.boost(p8.boostvector), p7.boost(p8.boostvector)
    assert p9.p == approx(p10.p), "Check boost to the C.O.M frame"
    p3_9, p3_10 = p9.vector, p10.vector
    assert p3_9.isopposite(p3_10)
    p8 = LorentzVector()
    p8.setptetaphie(10.,2E2,-2*(pi/3),20.) #sinh(eta) diverge quickly
    assert p8.theta() == 0.0
    assert p8.eta == 10E10

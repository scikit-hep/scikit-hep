from functools import partial

import pytest
from pytest import approx
import numpy as np
assert_allclose = partial(np.testing.assert_allclose, atol=.0000001)

from skhep.math.vectors import LorentzVector, Vector3D

ROOT = pytest.importorskip('ROOT')

def to_lv(rvec):
    if isinstance(rvec, ROOT.TLorentzVector):
        return LorentzVector(rvec.X(), rvec.Y(), rvec.Z(), rvec.T())
    else:
        return Vector3D(rvec.X(), rvec.Y(), rvec.Z())

def assert_same(lvec, rvec):
    assert_allclose(lvec, to_lv(rvec), atol=.0000001)

values = [-1, -.5, 0., .1, .5, 1., 2.32]
@pytest.mark.parametrize("x", values)
@pytest.mark.parametrize("y", values)
@pytest.mark.parametrize("z", values)
@pytest.mark.parametrize("t", values)
def test_values(x, y, z, t):
    np.seterr(divide='ignore', invalid='ignore')

    rvec = ROOT.TLorentzVector(x,y,z,t)
    svec = LorentzVector(x,y,z,t)

    assert_same(svec, rvec)
    assert_same(svec.boost_vector(), rvec.BoostVector())
    assert svec.p() == approx(rvec.P())
    assert svec.theta() == approx(rvec.Theta())
    # assert svec.cos_theta() == approx(rvec.CosTheta())
    assert svec.phi() == approx(rvec.Phi())
    assert svec.mag() == approx(rvec.Mag())
    assert svec.mag2() == approx(rvec.Mag2())
    # assert svec.rho() == approx(rvec.Rho())




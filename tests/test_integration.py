"""Cross-package integration tests for the scikit-hep metapackage.

These tests verify that the scikit-hep sub-packages listed in
requirements.txt can be imported together, in the same environment,
without version or namespace conflicts, and that a couple of
representative cross-package workflows behave as expected.

Deeper, per-package feature testing already lives in each package's
own test suite, and nightly cross-package regression testing across
main branches lives in https://github.com/scikit-hep/integration-tests.
This file intentionally stays small: it is a fast smoke test that a
`pip install scikit-hep` environment is internally consistent.

Issue: https://github.com/scikit-hep/scikit-hep/issues/398
"""

import importlib
import sys

import pytest

# Import names for every package bundled by the scikit-hep metapackage,
# as listed in requirements.txt. Keep this list in sync with that file.
SKHEP_PACKAGES = [
    "uproot",
    "awkward",
    "hist",
    "vector",
    "mplhep",
    "decaylanguage",
    "hepstats",
    "hepunits",
    "histoprint",
    "iminuit",
    "particle",
    "pylhe",
    "resample",
]


@pytest.mark.parametrize("package_name", SKHEP_PACKAGES)
def test_package_importable(package_name):
    """Each scikit-hep sub-package must import cleanly on its own."""
    if package_name == "hepstats" and sys.version_info >= (3, 13):
        pytest.skip("hepstats' zfit dependency does not yet support Python 3.13")
    module = importlib.import_module(package_name)
    assert module is not None


def test_no_import_conflicts():
    """All sub-packages must import together in a single process.

    This is the core integration check: if any two packages pin
    incompatible versions of a shared dependency, the import below
    will raise before we ever get to the assertions in the other
    tests.
    """
    for package_name in SKHEP_PACKAGES:
        if package_name == "hepstats" and sys.version_info >= (3, 13):
            continue
        importlib.import_module(package_name)


def test_awkward_vector_integration():
    """awkward arrays should interoperate with vector's behaviors.

    This is the main cross-package pattern used throughout HEP
    analyses: attaching vector's Lorentz/3D-vector methods to an
    awkward array via ``ak.with_name``.
    """
    import awkward as ak
    import vector

    vector.register_awkward()
    arr = ak.Array([{"x": 1.0, "y": 2.0, "z": 3.0}, {"x": 4.0, "y": 5.0, "z": 6.0}])
    vec_arr = ak.with_name(arr, "Vector3D")
    assert vec_arr.mag[0] == pytest.approx((1.0**2 + 2.0**2 + 3.0**2) ** 0.5)


def test_numpy_hist_integration():
    """hist should fill and summarize numpy data correctly.

    Confirms hist's basic compatibility with the wider scientific
    Python (numpy) ecosystem that the rest of scikit-hep relies on.
    """
    import numpy as np
    import hist

    data = np.random.default_rng(seed=42).normal(size=1000)
    h = hist.Hist.new.Reg(50, -5, 5, name="x").Double()
    h.fill(x=data)
    assert h.sum() == 1000

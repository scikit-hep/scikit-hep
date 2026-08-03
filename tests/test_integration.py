"""Integration tests for scikit-hep metapackage.

Issue: https://github.com/scikit-hep/scikit-hep/issues/398
"""

import importlib
import pytest

PACKAGES = [
    "awkward",
    "decaylanguage",
    "hepstats",
    "hepunits",
    "hist",
    "histoprint",
    "iminuit",
    "mplhep",
    "particle",
    "pylhe",
    "resample",
    "uproot",
    "vector",
]


@pytest.mark.parametrize("package_name", PACKAGES)
def test_package_imports(package_name):
    """Test that all required Scikit-HEP packages can be imported."""
    imported_module = importlib.import_module(package_name)
    assert imported_module is not None


def test_awkward_vector_integration():
    """Test awkward arrays work with vector operations."""
    import awkward
    import vector

    data = awkward.Array({"x": [1.0, 2.0, 3.0], "y": [1.0, 2.0, 3.0]})
    v = vector.array({"x": data["x"], "y": data["y"]})

    assert len(v) == 3
    assert v[0].x == 1.0
    assert v[0].y == 1.0


def test_hist_creation_with_numpy():
    """Test hist works with numpy data."""
    import hist
    import numpy as np

    h = hist.Hist(hist.axis.Regular(10, 0, 1, name="test"))
    data = np.random.uniform(0, 1, 100)
    h.fill(data)

    assert h.sum() == 100
    assert sum(h.view()) == 100


def test_multiple_packages_workflow():
    """Test a workflow using multiple packages together."""
    import awkward
    import hist
    import numpy as np

    data = awkward.Array({
        "x": np.random.uniform(0, 1, 100),
        "y": np.random.uniform(0, 1, 100),
    })

    h_x = hist.Hist(hist.axis.Regular(10, 0, 1))
    h_x.fill(data["x"])

    h_y = hist.Hist(hist.axis.Regular(10, 0, 1))
    h_y.fill(data["y"])

    assert sum(h_x.view()) == 100
    assert sum(h_y.view()) == 100


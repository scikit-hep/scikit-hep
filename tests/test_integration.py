"""Integration tests for scikit-hep metapackage.

These tests verify that all scikit-hep sub-packages
work correctly together when installed as a group.

Issue: https://github.com/scikit-hep/scikit-hep/issues/398

AI Usage: This test file was developed with assistance from
Claude AI for brainstorming test structure, code generation,
and documentation. All code has been reviewed and understood.
"""

import pytest


# Test that all key packages can be imported
@pytest.mark.parametrize(
    "module_name", ["uproot", "awkward", "hist", "vector", "mplhep"]
)
def test_package_imports(module_name):
    """Test that a package can be imported without errors.

    Parameters
    ----------
    module_name : str
        Name of the package to test import for
    """
    module = __import__(module_name)
    assert module is not None


def test_no_import_conflicts():
    """Test that all packages can be imported together without conflicts.

    This is the key integration test - verifies the metapackage
    doesn't have internal package version conflicts.
    """
    import uproot
    import awkward
    import hist
    import vector
    import mplhep

    # If we got here without ImportError, no conflicts!
    assert all([uproot, awkward, hist, vector, mplhep])


def test_awkward_vector_integration():
    """Test awkward arrays work with vector operations.

    Creates an awkward array with x, y coordinates and
    verifies that vector operations work on it.
    This ensures awkward and vector packages are compatible.
    """
    import awkward
    import vector

    # Create awkward array with x, y coordinates
    data = awkward.Array({"x": [1.0, 2.0, 3.0], "y": [1.0, 2.0, 3.0]})

    # Create vector from awkward data
    v = vector.array({"x": data["x"], "y": data["y"]})

    # Verify vector operations work
    assert len(v) == 3
    assert v[0].x == 1.0


def test_hist_with_numpy():
    """Test histogram creation works with numpy data.

    Verifies that hist package can process numpy arrays,
    a common workflow in HEP analysis.
    """
    import hist
    import numpy as np

    # Create histogram
    h = hist.Hist(hist.axis.Regular(10, 0, 1, name="test"))

    # Fill with random data
    data = np.random.uniform(0, 1, 100)
    h.fill(data)

    # Verify histogram created correctly
    assert h.sum() > 0
    assert sum(h.view()) == 100


def test_multi_package_workflow():
    """Test a realistic workflow using multiple packages together.

    This tests a typical HEP analysis pattern:
    1. Create data structure (awkward)
    2. Create histogram (hist)
    3. Process with multiple packages
    """
    import awkward
    import hist
    import numpy as np

    # Create sample data in awkward array
    data = awkward.Array(
        {"x": np.random.uniform(0, 1, 100), "y": np.random.uniform(0, 1, 100)}
    )

    # Create histograms from awkward data
    h_x = hist.Hist(hist.axis.Regular(10, 0, 1, name="x"))
    h_x.fill(data["x"])

    h_y = hist.Hist(hist.axis.Regular(10, 0, 1, name="y"))
    h_y.fill(data["y"])

    # Verify both histograms filled correctly
    assert sum(h_x.view()) == 100
    assert sum(h_y.view()) == 100

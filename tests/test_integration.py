"""Integration tests for scikit-hep metapackage.

These tests verify that all scikit-hep sub-packages
work correctly together when installed as a group.

Issue: https://github.com/scikit-hep/scikit-hep/issues/398
"""

import pytest


class TestPackageImports:
    """Test that all core packages can be imported together."""
    
    def test_uproot_import(self):
        """Test uproot can be imported."""
        import uproot
        assert uproot is not None
    
    def test_awkward_import(self):
        """Test awkward can be imported."""
        import awkward
        assert awkward is not None
    
    def test_hist_import(self):
        """Test hist can be imported."""
        import hist
        assert hist is not None
    
    def test_vector_import(self):
        """Test vector can be imported."""
        import vector
        assert vector is not None
    
    def test_mplhep_import(self):
        """Test mplhep can be imported."""
        import mplhep
        assert mplhep is not None
    
    def test_all_imports_together(self):
        """Test all packages import without conflicts."""
        import uproot
        import awkward
        import hist
        import vector
        import mplhep
        
        # If we got here, no import conflicts!
        assert all([uproot, awkward, hist, vector, mplhep])


class TestPackageIntegration:
    """Test that packages work together in realistic scenarios."""
    
    def test_awkward_vector_integration(self):
        """Test awkward arrays work with vector operations."""
        import awkward
        import vector
        
        # Create awkward array with x, y coordinates
        data = awkward.Array({
            "x": [1.0, 2.0, 3.0],
            "y": [1.0, 2.0, 3.0]
        })
        
        # Create vector from awkward data
        v = vector.array({
            "x": data["x"],
            "y": data["y"]
        })
        
        # Verify vector operations work
        assert len(v) == 3
        assert v[0].x == 1.0
        assert v[0].y == 1.0
    
    def test_hist_creation_with_numpy(self):
        """Test hist works with numpy data."""
        import hist
        import numpy as np
        
        # Create histogram
        h = hist.Hist(hist.axis.Regular(10, 0, 1, name="test"))
        
        # Fill with random data
        data = np.random.uniform(0, 1, 100)
        h.fill(data)
        
        # Verify histogram created correctly
        assert sum(h.view()) == 100  # All 100 events counted
    
    def test_multiple_packages_workflow(self):
        """Test a workflow using multiple packages together."""
        import awkward
        import hist
        import numpy as np
        
        # Create sample data in awkward array
        data = awkward.Array({
            "x": np.random.uniform(0, 1, 100),
            "y": np.random.uniform(0, 1, 100)
        })
        
        # Create histogram from awkward data
        h_x = hist.Hist(hist.axis.Regular(10, 0, 1, name="x"))
        h_x.fill(data["x"])
        
        h_y = hist.Hist(hist.axis.Regular(10, 0, 1, name="y"))
        h_y.fill(data["y"])
        
        # Both histograms should have 100 entries total
        assert sum(h_x.view()) == 100
        assert sum(h_y.view()) == 100


class TestPythonVersionCompatibility:
    """Test compatibility across Python versions.
    
    Note: This test runs on the current Python version.
    CI/CD should run this on all supported versions (3.9-3.13).
    """
    
    def test_all_packages_compatible_current_python(self):
        """Verify all packages work with current Python version."""
        import sys
        import uproot
        import awkward
        import hist
        import vector
        
        # This test simply ensures no Python version
        # incompatibilities cause import errors
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        # All packages imported successfully
        assert True
#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.dataset.defs module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest

from skhep.dataset.defs import *


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_base_classes():
    with pytest.raises(TypeError):
        Dataset.__init__()

def test_mixins():
    FromPersistent()
    ToPersistent()
    ConvertibleCopy()

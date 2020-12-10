#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        Dataset()


def test_mixins():
    FromPersistent()
    ToPersistent()
    ConvertibleCopy()
    ff = FromFiles()
    with pytest.raises(NotImplementedError):
        ff.from_file("non_existent_file")
    tf = ToFiles()
    with pytest.raises(NotImplementedError):
        tf.to_file("non_existent_file")
    np = NewNumpy()
    with pytest.raises(NotImplementedError):
        np.to_array()

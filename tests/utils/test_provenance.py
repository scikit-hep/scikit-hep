#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.utils.provenance module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import pytest

from skhep.utils import *
from skhep.utils.provenance import Provenance, Origin  # these are not imported automatically


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_base_classes():
    with pytest.raises(TypeError):
        Provenance.__init__()
    with pytest.raises(TypeError):
        Origin.__init__()

def test_ObjectOrigin():
    with pytest.raises(TypeError):
        ObjectOrigin.__init__()
    prov = ObjectOrigin('array_of_ints')
    assert prov.__repr__() == '<ObjectOrigin>'
    assert prov.detail == 'array_of_ints'

def test_FileOrigin():
    with pytest.raises(TypeError):
        FileOrigin.__init__()
    prov1 = FileOrigin('file.root')
    assert prov1.__repr__() == '<FileOrigin (1 file)>'
    assert prov1.detail == '"file.root"'
    prov1bis = FileOrigin(['file.root'])
    assert prov1bis.__repr__() == '<FileOrigin (1 file)>'
    assert prov1bis.detail == '"file.root"'
    prov3 = FileOrigin(['file1.root', 'file2.root','file3.root'])
    assert prov3.__repr__() == '<FileOrigin (3 files)>'
    assert prov3.detail == '"file1.root", "file2.root", "file3.root"'

def test_Transformation():
    with pytest.raises(TypeError):
        Transformation.__init__()
    transf = Transformation('all elms * 2')
    assert transf.__repr__() == '<Transformation(all elms * 2)>'
    assert transf.detail == 'all elms * 2 (, )'

def test_Formatting():
    with pytest.raises(TypeError):
        Formatting.__init__()

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
from skhep.utils.provenance import Provenance, Origin, MultiProvenance  # these are not imported automatically
from skhep.utils.exceptions import *


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------

def test_base_classes():
    with pytest.raises(TypeError):
        Provenance.__init__()
    with pytest.raises(TypeError):
        Origin.__init__()
    with pytest.raises(SkhepTypeError):
        Provenance()
    with pytest.raises(SkhepTypeError):
        Origin()

def test_ObjectOrigin():
    with pytest.raises(TypeError):
        ObjectOrigin()
    with pytest.raises(AssertionError):
        ObjectOrigin([1,2,3])
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
    assert prov3.detail == '"file1.root","file2.root","file3.root"'
    with pytest.raises(AssertionError):
        prov4 = FileOrigin([1,2,3])

def test_Transformation():
    with pytest.raises(TypeError):
        Transformation.__init__()
    transf = Transformation('all elms * 2')
    assert transf.__repr__() == '<Transformation(all elms * 2)>'
    assert transf.detail == 'all elms * 2'
    transf1 = Transformation('all elms * 2', "detail1", "detail2", transf)
    transf1.detail

def test_Formatting():
    with pytest.raises(TypeError):
        Formatting.__init__()
    forma = Formatting('ROOTDataset', 'DecayTree')
    assert forma.__repr__() == '<Formatting to ROOTDataset(DecayTree)>'
    assert forma.detail == 'ROOTDataset(DecayTree)'
    forma1 = Formatting('ROOTDataset', 'DecayTree', "detail1", forma)
    
def test_MultiProvenance():
    with pytest.raises(TypeError):
        MultiProvenance.__init__()
    with pytest.raises(ValueError):
        MultiProvenance("provenance")
    with pytest.raises(ValueError):
        MultiProvenance.__iadd__(MultiProvenance(),"provenance")
        
    prov1 = FileOrigin('file.root')
    multip = MultiProvenance(prov1)
    assert multip[0].__repr__() == '<FileOrigin (1 file)>'
    assert multip[0].detail == '"file.root"'
    assert multip.detail == '"file.root"'
    transf = Transformation('all elms * 2')
    multip += transf
    assert multip[1].__repr__() == '<Transformation(all elms * 2)>'
    assert multip[1].detail == 'all elms * 2'
    forma = Formatting('ROOTDataset', 'DecayTree')
    multip1 = multip.copy() + MultiProvenance(forma)
    assert multip1[2].__repr__() == '<Formatting to ROOTDataset(DecayTree)>'
    assert multip1[2].detail == 'ROOTDataset(DecayTree)'
    assert multip1.__repr__() == "0: {0} \n1: {1} \n2: {2}".format(prov1, transf, forma)
    multip2 = MultiProvenance(multip1)
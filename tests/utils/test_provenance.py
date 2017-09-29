#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Tests for the skhep.utils.provenance module.
"""

# -----------------------------------------------------------------------------
# Import statements
# -----------------------------------------------------------------------------
import unittest

from skhep.utils import *
from skhep.utils.provenance import Provenance, Origin  # these are not imported automatically


# -----------------------------------------------------------------------------
# Actual tests
# -----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_base_classes()
        self.test_ObjectOrigin()
        self.test_FileOrigin()
        self.test_Transformation()
        self.test_Formatting()

    def test_base_classes(self):
        self.assertRaises(TypeError, Provenance.__init__)
        self.assertRaises(TypeError, Origin.__init__)

    def test_ObjectOrigin(self):
        self.assertRaises(TypeError, ObjectOrigin.__init__)
        prov = ObjectOrigin('array_of_ints')
        self.assertEqual(prov.__repr__(),'<ObjectOrigin>')
        self.assertEqual(prov.detail,'array_of_ints')

    def test_FileOrigin(self):
        self.assertRaises(TypeError, FileOrigin.__init__)
        prov1 = FileOrigin('file.root')
        self.assertEqual(prov1.__repr__(), '<FileOrigin (1 file)>')
        self.assertEqual(prov1.detail, '"file.root"')
        prov1bis = FileOrigin(['file.root'])
        self.assertEqual(prov1bis.__repr__(), '<FileOrigin (1 file)>')
        self.assertEqual(prov1bis.detail, '"file.root"')
        prov3 = FileOrigin(['file1.root', 'file2.root','file3.root'])
        self.assertEqual(prov3.__repr__(), '<FileOrigin (3 files)>')
        self.assertEqual(prov3.detail, '"file1.root", "file2.root", "file3.root"')

    def test_Transformation(self):
        self.assertRaises(TypeError, Transformation.__init__)
        transf = Transformation('all elms * 2')
        self.assertEqual(transf.__repr__(), '<Transformation(all elms * 2)>')
        self.assertEqual(transf.detail, 'all elms * 2 (, )')

    def test_Formatting(self):
        self.assertRaises(TypeError, Formatting.__init__)

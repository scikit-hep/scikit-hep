#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
import unittest

from skhep.math import *
from skhep.utils.py23 import *

#-----------------------------------------------------------------------------
# Actual tests
#-----------------------------------------------------------------------------
class Test(unittest.TestCase):
    def runTest(self):
        # required for Python 2.6 only
        self.test_pdt()

    def test_pdt(self):
        pass

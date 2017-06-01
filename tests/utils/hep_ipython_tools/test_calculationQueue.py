# Licensed under a 3-clause BSD style license, see LICENSE.
from unittest import TestCase

from skhep.utils.hep_ipython_tools.calculation_queue import CalculationQueue, CalculationQueueItem
from skhep.utils.hep_ipython_tools.tests.fixtures import MockQueue


class A:
    pass


class TestCalculationQueue(TestCase):

    def setUp(self):
        self.calculation_queue = CalculationQueue()
        self.calculation_queue.queue = MockQueue()

    def test_put(self):
        a = A()

        self.calculation_queue.put("TestItem", "TestContent")
        self.calculation_queue.put("TestItem2", 2.34)
        self.calculation_queue.put("TestItem3", a)

        items = self.calculation_queue.queue.internal_storage

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0], CalculationQueueItem("TestItem", "TestContent"))
        self.assertEqual(items[1], CalculationQueueItem("TestItem2", 2.34))
        self.assertEqual(items[2], CalculationQueueItem("TestItem3", a))

    def test_fill_results_no_dubs(self):
        a = A()

        self.calculation_queue.put("TestItem", "TestContent")
        self.calculation_queue.put("TestItem2", 2.34)
        self.calculation_queue.put("TestItem3", a)

        self.calculation_queue.fill_results()

        self.assertEqual(self.calculation_queue.get("TestItem"), "TestContent")
        self.assertEqual(self.calculation_queue.get("TestItem2"), 2.34)
        self.assertEqual(self.calculation_queue.get("TestItem3"), a)

        self.assertIn("TestItem", self.calculation_queue.get_keys())
        self.assertIn("TestItem2", self.calculation_queue.get_keys())
        self.assertIn("TestItem3", self.calculation_queue.get_keys())

    def test_fill_results_dubs(self):
        self.calculation_queue.put("TestItem", "TestContent")
        self.calculation_queue.put("TestItem", 2.34)
        self.calculation_queue.put("TestItem2", "OtherContent")

        self.calculation_queue.fill_results()

        self.assertEqual(self.calculation_queue.get("TestItem"), 2.34)
        self.assertEqual(self.calculation_queue.get("TestItem2"), "OtherContent")

        self.assertIn("TestItem", self.calculation_queue.get_keys())
        self.assertIn("TestItem2", self.calculation_queue.get_keys())

# Licensed under a 3-clause BSD style license, see LICENSE.
import os
from time import sleep
from unittest import TestCase

from skhep.utils.hep_ipython_tools.calculation_process import CalculationProcess
from skhep.utils.hep_ipython_tools.calculation_queue import CalculationQueue
from tempfile import NamedTemporaryFile


class DerivedCalculationProcess(CalculationProcess):

    def start_process(self, **kwargs):
        self.result_queue.put("TestItem", "TestValue")
        self.result_queue.put("AnotherTestItem", "AnotherTestValue")


class OngoingCalculationProcess(CalculationProcess):

    def start_process(self, **kwargs):
        while True:
            sleep(1)


class LoggingCalculationProcess(CalculationProcess):

    def start_process(self, **kwargs):
        with open(self.log_file_name, "w") as f:
            f.write("Log File Content")


class TestCalculationProcess(TestCase):

    def get_terminated_process(self):
        queue = CalculationQueue()
        process = DerivedCalculationProcess(result_queue=queue, log_file_name=None, parameters=None)
        process.start()
        process.join()
        return process

    def test_invalid_result_queue(self):
        self.assertRaises(ValueError, DerivedCalculationProcess, result_queue=None,
                          log_file_name=None, parameters=None)

    def test_default_parameters(self):
        queue = CalculationQueue()
        process = DerivedCalculationProcess(result_queue=queue, log_file_name=None, parameters=None)

        self.assertFalse(process.is_alive())
        self.assertTrue(process.is_valid)

    def test_get_keys(self):
        process = self.get_terminated_process()

        keys = process.get_keys()

        self.assertIn("TestItem", keys)
        self.assertIn("AnotherTestItem", keys)

    def test_get(self):
        process = self.get_terminated_process()

        self.assertEqual(process.get("TestItem"), "TestValue")
        self.assertEqual(process.get("AnotherTestItem"), "AnotherTestValue")

        self.assertRaises(KeyError, process.get, "UnknownItem")

    def test_isAlive(self):
        process = self.get_terminated_process()

        self.assertFalse(process.is_alive())


class TestLoggingCalculationProcess(TestCase):

    def setUp(self):
        queue = CalculationQueue()

        self.tmp_file_name = NamedTemporaryFile(delete=False).name

        self.process = LoggingCalculationProcess(result_queue=queue, log_file_name=self.tmp_file_name,
                                                 parameters=None)

        self.process.start()
        self.process.join()

    def tearDown(self):
        self.process.terminate()

        if os.path.exists(self.tmp_file_name):
            os.unlink(self.tmp_file_name)

    def test_get_log(self):
        log_file_content = self.process.get_log()
        self.assertEqual(log_file_content, "Log File Content")

    def test_save_log(self):
        self.assertIsNone(self.process.log_file_content)
        self.assertEqual(self.tmp_file_name, self.process.log_file_name)

        self.process.save_log()

        self.assertEqual(self.process.log_file_content, "Log File Content")
        self.assertIsNone(self.process.log_file_name)

        self.assertFalse(os.path.exists(self.tmp_file_name))

    def test_log_already_there(self):
        self.process.log_file_content = "Already there"
        self.process.save_log()

        self.assertEqual(self.process.log_file_content, "Already there")


class TestOngoingCalculationProcess(TestCase):

    def setUp(self):
        queue = CalculationQueue()
        self.process = OngoingCalculationProcess(result_queue=queue, log_file_name=None, parameters=None)

    def tearDown(self):
        self.process.terminate()

    def test_get(self):
        self.process.start()

        self.assertEqual(self.process.get_keys(), None)
        self.assertEqual(self.process.get("TestItem"), None)


class TestOngoingLoggingCalculationProcess(TestCase):

    def setUp(self):
        self.tmp_file_name = NamedTemporaryFile(delete=False).name

        queue = CalculationQueue()
        self.process = OngoingCalculationProcess(result_queue=queue, log_file_name=self.tmp_file_name,
                                                 parameters=None)

    def tearDown(self):
        self.process.terminate()

        if os.path.exists(self.tmp_file_name):
            os.unlink(self.tmp_file_name)

    def test_get_log(self):
        self.process.start()

        self.assertEqual(self.process.get_log(), "")

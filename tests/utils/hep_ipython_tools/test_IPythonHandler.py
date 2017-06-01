# Licensed under a 3-clause BSD style license, see LICENSE.
import os
from unittest import TestCase

from skhep.utils.ipythontools.calculation_process import CalculationProcess
from skhep.utils.ipythontools.calculation import Calculation
from skhep.utils.ipythontools.calculation_queue import CalculationQueue
from skhep.utils.ipythontools.information import EnvironmentInformation
from skhep.utils.ipythontools.ipython_handler import IPythonHandler
from skhep.utils.ipythontools.tests.fixtures import MockQueue


class DeriviedCalculationProcess(CalculationProcess):

    def __init__(self, result_queue, log_file_name, parameters, some_variable, other_variable):
        CalculationProcess.__init__(self, result_queue, log_file_name, parameters)

        self.some_variable = some_variable
        self.other_variable = other_variable

    def start_process(self):
        pass


class DerivedCalculation(Calculation):

    def __init__(self):
        Calculation.__init__(self)
        self._calculation_process_type = DeriviedCalculationProcess


class DerivedIPythonHandler(IPythonHandler):

    def __init__(self):
        IPythonHandler.__init__(self)

        self._calculation_type = DerivedCalculation


class TestIPythonHandler(TestCase):

    def test_default(self):
        handler = IPythonHandler()

        self.assertEqual(handler.log_files, [])
        self.assertEqual(handler._calculation_type, Calculation)
        self.assertIsInstance(handler.information, EnvironmentInformation)

    def test_create_queue(self):
        queue = DerivedIPythonHandler.create_queue()

        self.assertIsInstance(queue, CalculationQueue)

        self.assertEqual(queue.get_keys(), [])
        self.assertEqual(queue.results, {})

    def test_next_log_file(self):

        handler = DerivedIPythonHandler()

        self.assertEqual(handler.log_files, [])

        next_log_file = handler.next_log_file_name()

        try:
            self.assertEqual(len(handler.log_files), 1)
            self.assertEqual(handler.log_files[0][1], next_log_file)

        finally:
            os.unlink(next_log_file)

    def test_many_next_log_files(self):
        handler = DerivedIPythonHandler()

        self.assertEqual(handler.log_files, [])

        next_log_files = [handler.next_log_file_name() for _ in range(200)]

        try:
            self.assertEqual(len(handler.log_files), 20)

            names = [log_file[1] for log_file in handler.log_files]
            self.assertEqual(names, next_log_files[-20:])

            for closed_log_file in next_log_files[:-20]:
                self.assertFalse(os.path.exists(closed_log_file))

        finally:
            for log_file_name in next_log_files:
                if os.path.exists(log_file_name):
                    os.unlink(log_file_name)

    def test_many_log_files_closed(self):
        handler = DerivedIPythonHandler()

        self.assertEqual(handler.log_files, [])

        next_log_files = [handler.next_log_file_name() for _ in range(100)]

        for log_file_name in next_log_files:
            if os.path.exists(log_file_name):
                os.unlink(log_file_name)

        next_log_files = [handler.next_log_file_name() for _ in range(100)]

        try:
            self.assertEqual(len(handler.log_files), 20)

            names = [log_file[1] for log_file in handler.log_files]
            self.assertEqual(names, next_log_files[-20:])

            for closed_log_file in next_log_files[:-20]:
                self.assertFalse(os.path.exists(closed_log_file))

        finally:
            for log_file_name in next_log_files:
                if os.path.exists(log_file_name):
                    os.unlink(log_file_name)

    def test_process_result_queue(self):
        handler = DerivedIPythonHandler()

        queue = CalculationQueue()
        queue.queue = MockQueue()

        queue.put("TestItem", "TestValue")

        calculation = handler.process(queue, some_variable=42, other_variable=21)

        self.assertEqual(len(calculation.process_list), 1)

        added_calculation = calculation.process_list[0]

        self.assertEqual(added_calculation.log_file_name, handler.log_files[0][1])
        self.assertEqual(added_calculation.result_queue, queue)
        self.assertEqual(added_calculation.result_queue.get_keys(), ["TestItem"])
        self.assertEqual(added_calculation.result_queue.get("TestItem"), "TestValue")
        self.assertEqual(added_calculation.parameters, None)
        self.assertEqual(added_calculation.some_variable, 42)
        self.assertEqual(added_calculation.other_variable, 21)

        self.assertEqual(calculation.get_keys(), ["TestItem"])
        self.assertEqual(calculation.get("TestItem"), "TestValue")
        self.assertEqual(calculation.get_parameters(), None)

    def test_process_no_result_queue(self):
        handler = DerivedIPythonHandler()

        calculation = handler.process(some_variable=42, other_variable=21)

        self.assertEqual(len(calculation.process_list), 1)

        added_calculation = calculation.process_list[0]

        result_queue = added_calculation.result_queue

        self.assertIsInstance(result_queue, CalculationQueue)

    def test_parameter_space_no_queue(self):
        handler = DerivedIPythonHandler()

        def creator_function(some_variable, other_variable):
            return dict(some_variable=some_variable + 1, other_variable=other_variable + "c")

        calculations = handler.process_parameter_space(creator_function,
                                                       some_variable=[1, 2], other_variable=["a", "b"])

        self.assertEqual(len(calculations.process_list), 4)

        parameters = calculations.get_parameters()

        self.assertIn({"some_variable": 1, "other_variable": "a"}, parameters)
        self.assertIn({"some_variable": 1, "other_variable": "b"}, parameters)
        self.assertIn({"some_variable": 2, "other_variable": "a"}, parameters)
        self.assertIn({"some_variable": 2, "other_variable": "b"}, parameters)

        def assert_is_in_processes(some_variable, other_variable):
            for process in calculations.process_list:
                if process.some_variable == some_variable and process.other_variable == other_variable:
                    return True

            self.fail()

        assert_is_in_processes(2, "ac")
        assert_is_in_processes(3, "ac")
        assert_is_in_processes(2, "bc")
        assert_is_in_processes(3, "bc")

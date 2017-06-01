# Licensed under a 3-clause BSD style license, see LICENSE.
from unittest import TestCase
from skhep.utils.hep_ipython_tools.calculation import Calculation
from skhep.utils.hep_ipython_tools.calculation_process import CalculationProcess
from skhep.utils.hep_ipython_tools.calculation_queue import CalculationQueue


class TestCalculation(TestCase):

    def test_default(self):
        calculation = Calculation()

        self.assertEqual(calculation._calculation_process_type, CalculationProcess)
        self.assertEqual(calculation.process_list, [])

        calculations = Calculation([1, 2, 3])
        self.assertEqual(calculations.process_list, [1, 2, 3])

    def test_iter(self):
        calculations = Calculation([0, 1, 2])

        for i, calc in enumerate(calculations):
            self.assertEqual(calc.process_list, [i])

        self.assertEqual(len(calculations), 3)

    def test_is_running(self):
        calculations, process = self.create_calculations()

        process.is_alive = lambda: True
        self.assertEqual(calculations.is_running(), [False, True, False])

    def test_is_finished(self):
        calculations, process = self.create_calculations()

        process.already_run = lambda: True
        self.assertEqual(calculations.is_finished(), [False, True, False])

    def test_map_on_process(self):
        calculations, process = self.create_calculations()

        process.is_alive = lambda: True

        self.assertEqual(calculations.map_on_processes(lambda p: p.is_alive(), index=None), [False, True, False])
        self.assertEqual(calculations.map_on_processes(lambda p: p.is_alive(), index=1), True)
        self.assertEqual(calculations.map_on_processes(lambda p: p.is_alive(), index=0), False)
        self.assertEqual(calculations.map_on_processes(lambda p: p.is_alive(), index=process), True)

    def create_calculations(self):
        process1 = CalculationProcess(CalculationQueue(), None, None)
        process2 = CalculationProcess(CalculationQueue(), None, None)
        process3 = CalculationProcess(CalculationQueue(), None, None)

        calculations = Calculation([process1, process2, process3])

        return calculations, process2

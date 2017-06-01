# Licensed under a 3-clause BSD style license, see LICENSE.
from unittest import TestCase
from skhep.utils.ipythontools.calculation_list import create_every_parameter_combination, create_all_calculations


class TestCalculationList(TestCase):

    def test_create_every_parameter_combination(self):

        parameter_names = ["A", "B", "C"]
        parameter_values = [
            [1, 2],
            ["a", "b"],
            ["(", ")"]
        ]

        every_parameter_combination = create_every_parameter_combination(parameter_names,
                                                                         parameter_values)

        self.assertEqual(len(every_parameter_combination), 8)

        self.assertIn({"A": 1, "B": "a", "C": "("}, every_parameter_combination)
        self.assertIn({"A": 1, "B": "a", "C": ")"}, every_parameter_combination)
        self.assertIn({"A": 1, "B": "b", "C": "("}, every_parameter_combination)
        self.assertIn({"A": 1, "B": "b", "C": ")"}, every_parameter_combination)
        self.assertIn({"A": 2, "B": "a", "C": "("}, every_parameter_combination)
        self.assertIn({"A": 2, "B": "a", "C": ")"}, every_parameter_combination)
        self.assertIn({"A": 2, "B": "b", "C": "("}, every_parameter_combination)
        self.assertIn({"A": 2, "B": "b", "C": ")"}, every_parameter_combination)

    def test_create_all_calculations_no_queue(self):
        def creator_function(x, y):
            return {"a": 2 * x, "b": y + 1}

        all_calculation_kwargs, all_queues, every_parameter_combination = create_all_calculations(creator_function,
                                                                                                  x=[1, 2], y=[3, 4])

        all_calculation_kwargs = list(all_calculation_kwargs)
        all_queues = list(all_queues)
        every_parameter_combination = list(every_parameter_combination)

        self.assertEqual(len(all_calculation_kwargs), 4)
        self.assertEqual(len(all_queues), 4)
        self.assertEqual(len(every_parameter_combination), 4)

        self.assertIn({"x": 1, "y": 3}, every_parameter_combination)
        self.assertIn({"x": 1, "y": 4}, every_parameter_combination)
        self.assertIn({"x": 2, "y": 3}, every_parameter_combination)
        self.assertIn({"x": 2, "y": 4}, every_parameter_combination)

        for combination in [{"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]:
            index = every_parameter_combination.index(combination)
            x = combination["x"]
            y = combination["y"]
            self.assertEqual(all_calculation_kwargs[index], {"a": 2 * x, "b": y + 1})

    def test_create_all_calculations_queue(self):
        def creator_function(x, y, queue):
            return {"a": 2 * x, "b": y + 1, "queue": queue}

        all_calculation_kwargs, all_queues, every_parameter_combination = create_all_calculations(creator_function,
                                                                                                  x=[1, 2], y=[3, 4])

        all_calculation_kwargs = list(all_calculation_kwargs)
        all_queues = list(all_queues)
        every_parameter_combination = list(every_parameter_combination)

        self.assertEqual(len(all_calculation_kwargs), 4)
        self.assertEqual(len(all_queues), 4)
        self.assertEqual(len(every_parameter_combination), 4)

        self.assertIn({"x": 1, "y": 3}, every_parameter_combination)
        self.assertIn({"x": 1, "y": 4}, every_parameter_combination)
        self.assertIn({"x": 2, "y": 3}, every_parameter_combination)
        self.assertIn({"x": 2, "y": 4}, every_parameter_combination)

        for combination in [{"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]:
            index = every_parameter_combination.index(combination)
            x = combination["x"]
            y = combination["y"]
            self.assertEqual(all_calculation_kwargs[index], {"a": 2 * x, "b": y + 1, "queue": all_queues[index]})

    def test_create_all_calculations_none(self):
        def creator_function(x, y):
            if x > 1:
                return None
            return {"a": 2 * x, "b": y + 1}

        all_calculation_kwargs, all_queues, every_parameter_combination = create_all_calculations(creator_function,
                                                                                                  x=[1, 2], y=[3, 4])
        all_calculation_kwargs = list(all_calculation_kwargs)
        all_queues = list(all_queues)
        every_parameter_combination = list(every_parameter_combination)

        self.assertEqual(len(all_calculation_kwargs), 4)
        self.assertEqual(len(all_queues), 4)
        self.assertEqual(len(every_parameter_combination), 4)

        self.assertIn({"a": 2, "b": 4}, all_calculation_kwargs)
        self.assertIn({"a": 2, "b": 5}, all_calculation_kwargs)
        self.assertNotIn({"a": 4, "b": 4}, all_calculation_kwargs)
        self.assertNotIn({"a": 4, "b": 5}, all_calculation_kwargs)

        for combination in [{"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]:
            index = every_parameter_combination.index(combination)
            x = combination["x"]
            y = combination["y"]

            if x == 1:
                self.assertEqual(all_calculation_kwargs[index], {"a": 2 * x, "b": y + 1})
            else:
                self.assertEqual(all_calculation_kwargs[index], None)

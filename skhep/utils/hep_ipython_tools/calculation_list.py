# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import

try:
    from funcsigs import signature
except ImportError:
    from inspect import signature
import itertools

from . import calculation_queue


def create_all_calculations(parameter_creator_function, **calculation_lists):
    """
    Create all calculations.
    :param calculation_lists:
    :param parameter_creator_function:
    """

    parameter_names_in_list = calculation_lists.keys()
    parameter_values_in_list = calculation_lists.values()

    every_parameter_combination = create_every_parameter_combination(parameter_names_in_list,
                                                                     parameter_values_in_list)

    all_queues = [calculation_queue.CalculationQueue() for _ in every_parameter_combination]

    def add_queue_if_needed(c_queue, param_combination):
        param_combination_copy = param_combination.copy()
        args = signature(parameter_creator_function).parameters
        if "queue" in args:
            param_combination_copy.update({"queue": c_queue})

        return param_combination_copy

    every_parameter_combination_with_queue = [add_queue_if_needed(c_queue, parameters) for
                                              c_queue, parameters in zip(all_queues, every_parameter_combination)]

    def call_creator(param_combination):
        calculation_kwargs = parameter_creator_function(**param_combination)
        return calculation_kwargs

    all_calculation_kwargs = map(call_creator, every_parameter_combination_with_queue)
    return all_calculation_kwargs, all_queues, every_parameter_combination


def create_every_parameter_combination(parameter_names, parameter_values):
    """
    Combine all parameter values with all other parameter values and form dictionaries with the correct
    names.
    :param parameter_names: A list of names of the parameters.
    :param parameter_values: A list of lists with parameter values. Each list stands for one parameter
        (so the len of parameter_names must be the len of parameter_value).
    :return: A list of dictionaries, each a single combination of parameters.
    """

    assert len(parameter_names) == len(parameter_values)

    every_parameter_combination = itertools.product(*parameter_values)
    every_parameter_combination_with_names = [
        {parameter_name: value for parameter_name, value in zip(
            parameter_names, values)} for values in every_parameter_combination]
    return every_parameter_combination_with_names

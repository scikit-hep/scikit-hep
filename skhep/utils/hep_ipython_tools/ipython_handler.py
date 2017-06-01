# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import

import os
import tempfile

from . import calculation_queue, calculation, information, calculation_list


class IPythonHandler:

    """
    Handler class to start processes in an IPython notebook in a convenient way.
    From this whole framework you should not need to create any instances by yourself but rather use the
    given ipython handler for this.

    Usage
    -----

    Create a handler object in the beginning of your NB and use the two methods `process`
    and `process_parameter_space` to turn parameters or a parameter creator function into a Calculation.
    Do not create calculations on you own.

        from tracking.validation.ipython_handler import handler

        calculation = handler.process(parameters)

    """

    def __init__(self):
        """
        Each created log file gets registered and deleted if there are more than 20 log files present
        or if the get_log function of the process is called (the log is saved elsewhere).
        As the log files are saved to /tmp you have probably not to care about deleting them.
        """

        #: A list of open log files.
        self.log_files = []

        #: A shortcut for returning information on the environment.
        self.information = information.EnvironmentInformation()

        #: The calculation type to use
        self._calculation_type = calculation.Calculation

    def process(self, result_queue=None, **kwargs):
        """
        Turn a parameter set into a Calculation that you can start, stop or whatever you want.

        Arguments
        ---------
        result_queue: The CalculationQueue you want to use. Without giving this as a parameter
           the function creates one for you. Create one on your own with the function create_queue.
        """

        if result_queue is None:
            result_queue = calculation_queue.CalculationQueue()

        calculation = self._calculation_type()
        calculation.append(result_queue=result_queue, log_file_name=self.next_log_file_name(), parameters=None, **kwargs)

        return calculation

    def process_parameter_space(self, kwargs_creator_function, **parameter_lists):
        """
        Create a list of calculations by combining all parameters with all parameters you provide and
        feeding the tuple into the parameter_creator_function.
        If the kwargs_creator_function has a parameter named queue, the function feeds the corresponding
        created queue into the parameter_creator_function.
        The parameter_creator_function must return a dictionary for every combination of parameters it gets,
        which will be used to construct a process out of it.
        See ipython_handler_basf2/ipython_handler for an example.

        Please note that a list of calculations acts the same as a single calculation you would get from
        the process function. You can handle 10 calculations the same way you would handle a single one.

        The kwargs_creator_function can transform the incoming parameters into different ones. To make this
        more clear, the resulting dictionary created by the kwargs_creator_function is called kwargs.
        These are the ones, that will be used to create a calculation process, so they must be compatible to the
        calculation you chose (namely compatible with the append function of the _calculation_type).

        Arguments
        ---------
        kwargs_creator_function: A function with as many input parameters as parameters you provide.
           If the function has an additional queue parameter it is fed with the corresponding queue for this calculation.
        parameter_lists: As many lists as you want. Every list is one parameter. If you do not want a
           specific parameter constellation to occur, you can return None in your parameter_creator_function for
           this combination.

        Usage
        -----
            def kwargs_creator_function(par_1, par_2, par_3, queue):
                kwargs = {... f(par_1) ... g(par_2) ... h(par_3)}
                queue.put(..., ...)
                return kwargs

            calculations = handler.process_parameter_space(kwargs_creator_function,
                                                           par_1=[1, 2, 3], par_2=["x", "y", "z"], par_3=[3, 4, 5])

        The calculations will be created with the kwargs arguments.
        """

        all_kwargs, all_queues, all_parameters = calculation_list.create_all_calculations(kwargs_creator_function,
                                                                                          **parameter_lists)

        calculations = self._calculation_type()

        for kwargs, q, parameters in zip(all_kwargs, all_queues, all_parameters):
            calculations.append(result_queue=q, log_file_name=self.next_log_file_name(),
                                parameters=parameters, **kwargs)

        return calculations

    def next_log_file_name(self):
        """
        Return the name of the next log file.
        If there are more than 20 log files present,
        start deleting the oldest ones.
        """
        next_log_file = tempfile.mkstemp()
        self.log_files.append(next_log_file)
        while len(self.log_files) > 20:
            first_log_file = self.log_files.pop(0)
            f = first_log_file[0]
            log_file_name = first_log_file[1]

            os.close(f)
            try:
                os.unlink(log_file_name)
            except OSError:
                pass
        return next_log_file[1]

    @staticmethod
    def create_queue():
        """
        Create a Calculation queue. You need to do this if you want to pass it to your modules
        and write to it while processing the events.
        """
        return calculation_queue.CalculationQueue()

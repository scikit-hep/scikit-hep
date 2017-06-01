# Licensed under a 3-clause BSD style license, see LICENSE.
import os
from multiprocessing import Process, Pipe


class CalculationProcess(Process):
    """
    Abstract base class for doing the real processing of a calculation. Is used by the handler to
    process the calculation you requested. Overload the start_process and prepare method to implement your calculation
    and maybe also the __init__ method if you need to store more information on your process (like what to calculate).

    See ipython_handler_basf2/calculation_process.py for an example implementation.
    """

    def __init__(self, result_queue, log_file_name, parameters):
        """
        Create a new calculation process instance. The parameters here are the absolute standard. You probably have to redefine the
        constructor in your own class.
        """
        if result_queue is None:
            raise ValueError("Invalid result_queue")

        #: True if already started/run
        self.already_run = False

        #: Name of the log file to use
        self.log_file_name = log_file_name

        #: Saved log file content after the run
        self.log_file_content = None

        #: Result queue as a reference
        self.result_queue = result_queue

        #: Parameters in process_parameter_space
        self.parameters = parameters

        #: Create the queue for the progress python module
        self.progress_queue_local, self.progress_queue_remote = Pipe()

        #: Set to false, if you do not want this process to show up in the process bar calculations
        self.is_valid = True

        # Prepare the environment.
        self.prepare()

        # Call the constructor of the base class.
        Process.__init__(self, target=self.start_process)

    def save_log(self):
        """
        Delete the log file and copy its content to the class.
        """
        if self.log_file_content is None:
            with open(self.log_file_name) as f:
                self.log_file_content = f.read()
            os.unlink(self.log_file_name)
            self.log_file_name = None

    def get_log(self):
        """
        Return the log file content.
        Use the methods of the Calculation for a better handling.
        """
        if self.is_alive():
            with open(self.log_file_name) as f:
                return f.read()
        else:
            self.save_log()
            return self.log_file_content

    def get(self, name):
        """
        Return an item from the result queue. Only gives a result if the calculation has finished.
        Use the Calculation for a better handling.
        """
        if not self.is_alive():
            return self.result_queue.get(name)

    def get_keys(self):
        """
        Return the names of all item from the result queue. Only gives a result if the calculation has finished.
        Use the Calculation for a better handling.
        """
        if not self.is_alive():
            return self.result_queue.get_keys()

    def start_process(self):
        """
        The function given to the process to start the calculation.
        Do not call by yourself.
        Resets the logging system, logs onto console and a file and sets the queues
        (the result queue and the process queue) correctly.
        """
        pass

    def prepare(self):
        """
        Overload this function if you need to process some preparations
        before doing the real calculation.
        """
        pass

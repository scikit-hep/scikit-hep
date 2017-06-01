# Licensed under a 3-clause BSD style license, see LICENSE.
from multiprocessing import Queue

try:
    from queue import Empty
except ImportError:
    from Queue import Empty


class CalculationQueue:
    """
    This class is a wrapper around a multiprocessing.Queue

    It can be used to send and receive values from the modules while processing the calculation.
    You can use it to save - for example - filepaths of outputfiles that you create on the fly.
    The added items are all of the type CalculationQueueItem.
    The CalculationQueue can be used as a dict. After the termination of the underlaying process
    you can access the different entries by their names you gave them when putting them on the queue.
    """

    def __init__(self):
        """
        Create a queue.
        """
        #: The multiprocessing queue to handle
        self.queue = Queue()
        #: The results to be filled in the end
        self.results = dict()

    def put(self, name, item, **kwargs):
        """
        Put an item on the queue with the given name. Please keep that adding two items with the same name
        overrides one of them!
        """
        self.queue.put(CalculationQueueItem(name, item), block=True, **kwargs)

    def fill_results(self):
        """
        Fill the internal dict with the information of the queue.
        Do not call this on your own.
        Do only call this when the underlying process has ended.
        """
        while True:
            try:
                result = self.queue.get_nowait()
                self.results.update({result.name: result.item})
            except Empty:
                return

    def get(self, name):
        """
        Return the item with the given name or an Exception when it is not found.
        Do not call this on your own..
        """
        self.fill_results()
        return self.results[name]

    def get_keys(self):
        """
        Return all possible names of items saved in this queue.
        Do not call this on your own.
        """
        self.fill_results()
        return list(self.results.keys())


class CalculationQueueItem:
    """
    A placeholder for a tuple string, object.
    Do not create them by yourself.
    """

    def __init__(self, name, item):
        """
        Create a new queue item
        """
        #: Name of the item
        self.name = name
        #: Item to store
        self.item = item

    def __eq__(self, other):
        """
        Equality operator needed for tests.
        """
        return other.name == self.name and other.item == self.item

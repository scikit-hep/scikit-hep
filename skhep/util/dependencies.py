# Licensed under a 3-clause BSD style license, see LICENSE.

class DelayedImportError(object):
    def __init__(self, err):
        self.err = err

    def __getattr__(self, attr):
        raise self.err

def softimport(modulename):
    try:
        return __import__(modulename)
    except ImportError as err:
        return DelayedImportError(err)

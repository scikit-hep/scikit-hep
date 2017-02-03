# Licensed under a 3-clause BSD style license, see LICENSE.

class DelayedImportError(object):
    def __init__(self, err):
        self.err = err

    def __getattr__(self, attr):
        raise self.err

class LazyModule(object):
    def __init__(self, name):
        self.name = name
        self.module = None

    def __getattr__(self, attr):
        if self.module is None:
            self.module = __import__(self.name)
        return getattr(self.module, attr)

# Two ideas:
# 
# Strict softimport tries to load at startup (like a normal Python import)
# but hides the fact that it failed until the user tries to use it.
# 
# Lazy softimport doesn't even try to load until the user tries to use it.
#
# Both have the same semantics: the user only needs to have installed the
# dependencies he or she will need. But strict puts all the load-time at
# startup while lazy puts all the load-time at first use.
#
# We should have a policy and stick to it. Strict is more typical of Python
# modules, but lazy would spare the user the 1.09 second lag on startup
# if they have ROOT on their system but don't intend to use it in this session.

def softimport(modulename, lazy=False):
    if lazy:
        return LazyModule(modulename)
    else:
        try:
            return __import__(modulename)
        except ImportError as err:
            return DelayedImportError(err)

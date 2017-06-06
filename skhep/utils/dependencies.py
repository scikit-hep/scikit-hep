# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Submodule for helpers to deal with dependencies
===============================================
"""

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
#
# **Edit:** Another advantage of lazy softimport: if the user tries to use the
# module, it fails with an ImportError, then they install it and try to use
# it again in the same Python session, this will work with lazy softimport
# and not with strict softimport. For this reason, I'm changing the default
# to lazy=True and would advocate that we _only_ do lazy softimports.


class DelayedImportError(object):
    # When a module is strictly softimported but is not available, this
    # object is a placeholder for the module. The user will get the
    # original error when they try to use it.

    def __init__(self, err):
        self.err = err

    def __getattr__(self, attr):
        raise self.err


class LazyModule(object):
    # When a module is lazily softimported, it will always be represented
    # with this object as a placeholder. It will repeatedly attempt to
    # import the module every time the user tries to use it (unlike strict,
    # which gives up after the first attempt on startup).
    #
    # Unlike strict, the module will always be wrapped by this object,
    # even if the module is available. Users will be able to see
    # the sausage-making if they're inclined to do `type(root_numpy)`.

    def __init__(self, name):
        self.name = name
        self.module = None

    def __getattr__(self, attr):
        if self.module is None:
            self.module = __import__(self.name)
        return getattr(self.module, attr)


def softimport(modulename, lazy=True):
    """
    The function that one calls to import a module softly.
    """
    # Once we vote on "always strict" or "always lazy," we should _take out_
    # the other functionality so that it isn't even an option.

    if lazy:
        return LazyModule(modulename)
    else:
        try:
            return __import__(modulename)
        except ImportError as err:
            return DelayedImportError(err)

# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Submodule for decorators
========================

Note: not meant for user code in general, though possible.
"""


def inheritdoc(cls, gap="\n\n"):
    """
    Decorator to automatize the inheritance of documentation from a class method.

    :Example:
    >>> from skhep.utils.decorators import inheritdoc
    >>> class ADerivedClass(ABaseClass):                 # doctest: +SKIP
    ...    @inheritdoc(ABaseClass)                       # doctest: +SKIP
    ...    def amethod(self): pass                       # doctest: +SKIP
    """
    def _fn(fn):
        if fn.__name__ in cls.__dict__:
            if fn.__doc__ is None:
                fn.__doc__ = cls.__dict__[fn.__name__].__doc__
            else:
                fn.__doc__ = cls.__dict__[
                    fn.__name__].__doc__.strip() + gap + fn.__doc__.strip()
        return fn
    return _fn

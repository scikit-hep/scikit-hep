# Licensed under a 3-clause BSD style license, see LICENSE.

def inheritdoc(cls, gap="\n\n"):
    def _fn(fn):
        if fn.__name__ in cls.__dict__:
            if fn.__doc__ is None:
                fn.__doc__ = cls.__dict__[fn.__name__].__doc__
            else:
                fn.__doc__ = cls.__dict__[fn.__name__].__doc__.strip() + gap + fn.__doc__.strip()
        return fn
    return _fn

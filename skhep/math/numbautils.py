# This is a set of utility functions for vectors. Feel free to use them alone if needed. These are ufuncts if numba is present.

from __future__ import division, print_function, absolute_import


try:
    from numba import float32, float64, int32, int64, bool_, jit, vectorize, types, guvectorize
    from numba.extending import overload_method, overload

except ImportError:
    float32 = []
    float64 = []
    def jit(*args, **kargs):
        def copyf(function):
            return function
        return copyf
    vectorize = jit
    overload_method = jit
    overload = jit
    class types:
        Array = None



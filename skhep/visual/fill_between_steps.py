from __future__ import absolute_import
import numpy as np
import numpy.ma as ma
import collections


def fill_between_steps(ax, x, y1, y2=0, step_where='pre', **kwargs):
    ''' Fill between for a step plot histogram.
    Modified from original code produced by T. Caswell (https://github.com/tacaswell).

    Parameters
    ----------
    ax : Axes
       The axes to draw to

    x : array-like
        Array/vector of index values.

    y1 : array-like or float
        Array/vector of values to be filled under.
    y2 : array-Like or float, optional
        Array/vector or bottom values for filled area. Default is 0.

    step_where : {'pre', 'post', 'mid'}
        where the step happens, same meanings as for `step`

    **kwargs will be passed to the matplotlib fill_between() function.

    Returns
    -------
    ret : PolyCollection
       The added artist

    '''

    # Modification to account for histogram-like bin-edges
    if len(x) == len(y1)+1 and len(y1) != 1:
        kwargs['linewidth'] = 0
        if isinstance(y2, collections.Container):
            y2_trunc = y2[0:2]
        else:
            y2_trunc = y2
        fill_between_steps(ax, x[0:2], y1[0:2], y2=y2_trunc, step_where='post', **kwargs)
        kwargs['label'] = None
        return fill_between_steps(ax, x[1:], y1, y2=y2, step_where='pre', **kwargs)

    # Account for case in which there is exactly one bin
    elif len(y1) == 1:
        y1 = y1[0]
        if isinstance(y2, collections.Container):
            y2 = y2[0]
        else:
            y2 = y2

    if step_where not in ['pre', 'post', 'mid']:
        raise ValueError("where must be one of {{'pre', 'post', 'mid'}} "
                         "You passed in {wh}".format(wh=step_where))

    # make sure y values are up-converted to arrays
    if np.isscalar(y1):
        y1 = np.ones_like(x) * y1

    if np.isscalar(y2):
        y2 = np.ones_like(x) * y2

    # temporary array for up-converting the values to step corners
    # 3 x 2N - 1 array

    vertices = np.vstack((x, y1, y2))

    # this logic is lifted from lines.py
    # this should probably be centralized someplace
    if step_where == 'pre':
        steps = ma.zeros((3, 2 * len(x) - 1), np.float)
        steps[0, 0::2], steps[0, 1::2] = vertices[0, :], vertices[0, :-1]
        steps[1:, 0::2], steps[1:, 1:-1:2] = vertices[1:, :], vertices[1:, 1:]

    elif step_where == 'post':
        steps = ma.zeros((3, 2 * len(x) - 1), np.float)
        steps[0, ::2], steps[0, 1:-1:2] = vertices[0, :], vertices[0, 1:]
        steps[1:, 0::2], steps[1:, 1::2] = vertices[1:, :], vertices[1:, :-1]

    elif step_where == 'mid':
        steps = ma.zeros((3, 2 * len(x)), np.float)
        steps[0, 1:-1:2] = 0.5 * (vertices[0, :-1] + vertices[0, 1:])
        steps[0, 2::2] = 0.5 * (vertices[0, :-1] + vertices[0, 1:])
        steps[0, 0] = vertices[0, 0]
        steps[0, -1] = vertices[0, -1]
        steps[1:, 0::2], steps[1:, 1::2] = vertices[1:, :], vertices[1:, :]
    else:
        raise RuntimeError("should never hit end of if-elif block for validated input")

    # un-pack
    xx, yy1, yy2 = steps

    # now to the plotting part:
    return ax.fill_between(xx, yy1, y2=yy2, **kwargs)

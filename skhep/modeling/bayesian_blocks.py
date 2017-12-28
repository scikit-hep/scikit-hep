# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Bayesian Block implementation
=============================

Dynamic programming algorithm for finding the optimal adaptive-width histogram.

* Based on Scargle et al 2012 [1]_
* Initial Python Implementation [2]_
* AstroML Implementation [3]_

References
----------
.. [1] http://adsabs.harvard.edu/abs/2012arXiv1207.5578S
.. [2] http://jakevdp.github.com/blog/2012/09/12/dynamic-programming-in-python/
.. [3] https://github.com/astroML/astroML/blob/master/astroML/density_estimation/bayesian_blocks.py
"""
from __future__ import absolute_import
from __future__ import division
from skhep.utils.py23 import *
import numpy as np
import pandas as pd


class Events(object):
    def __init__(self, p0=0.05, gamma=None):
        self.p0 = p0
        self.gamma = gamma

    def fitness(self, N_k, T_k):
        # eq. 19 from Scargle 2012
        return N_k * (np.log(N_k) - np.log(T_k))

    def prior(self, N, Ntot):
        if self.gamma is not None:
            return -np.log(self.gamma)
        else:
            # eq. 21 from Scargle 2012
            return 4 - np.log(73.53 * self.p0 * (N ** -0.478))

    # the fitness_args property will return the list of arguments accepted by
    # the method fitness().  This allows more efficient computation below.
    @property
    def args(self):
        try:
            # Python 2
            return self.fitness.func_code.co_varnames[1:]
        except AttributeError:
            return self.fitness.__code__.co_varnames[1:]


def bayesian_blocks(data, weights=None, p0=0.05, gamma=None):
    """Bayesian Blocks Implementation.

    This is a flexible implementation of the Bayesian Blocks algorithm described in Scargle 2012
    [1]_.  It has been modified to natively accept weighted events, for ease of use in HEP
    applications.

    Args:
        data (array):
            Input data values (one dimensional, length N). Repeat values are allowed.

        weights (array_like, optional):
            Weights for data (otherwise assume all data points have a weight of 1).  Must be same
            length as data.

            Defaults to None.

        p0 (float, optional):
            False-positive rate, between 0 and 1.  A lower number places a stricter penalty against
            creating more bin edges, thus reducing the potential for false-positive bin edges.

            Defaults to 0.05.

        gamma (float, optional):
            If specified, then use this gamma to compute the general prior form, p ~ gamma^N. If
            gamma is specified, p0 is ignored.

            Defaults to None.


    Returns:
        edges (ndarray):
            Array containing the (N+1) bin edges

    Examples:
        Event data:

        >>> d = np.random.normal(size=100)
        >>> bins = bayesian_blocks(d, p0=0.01)

        Event data with repeats:

        >>> d = np.random.normal(size=100)
        >>> d[80:] = d[:20]
        >>> bins = bayesian_blocks(d, p0=0.01)

        Event data with weights:

        >>> d = np.random.normal(size=100)
        >>> w = np.random.uniform(1,2, size=100)
        >>> bins = bayesian_blocks(d, w, p0=0.01)


    See Also:
        skhep.visual.MplPlotter.hist:
            Histogram plotting function which can natively make use of bayesian blocks.
    """
    # validate input data
    data = np.asarray(data, dtype=float)
    assert data.ndim == 1

    # validate input weights
    if weights is not None:
        weights = np.asarray(weights)
    else:
        # set them to 1 if not given
        weights = np.ones_like(data)

    # verify the fitness function
    fitfunc = Events(p0, gamma)

    # Place data and weights into a DataFrame.
    # We want to sort the data array (without losing the associated weights), and combine duplicate
    # data points by summing their weights together.  We can accomplish all this with `groupby`

    df = pd.DataFrame({'data': data, 'weights': weights})
    gb = df.groupby('data').sum()
    data = gb.index.values
    weights = gb.weights.values

    N = weights.size

    # create length-(N + 1) array of cell edges
    edges = np.concatenate([data[:1],
                            0.5 * (data[1:] + data[:-1]),
                            data[-1:]])
    block_length = data[-1] - edges

    # arrays to store the best configuration
    best = np.zeros(N, dtype=float)
    last = np.zeros(N, dtype=int)

    # -----------------------------------------------------------------
    # Start with first data cell; add one cell at each iteration
    # -----------------------------------------------------------------
    for R in range(N):
        # Compute fit_vec : fitness of putative last block (end at R)
        kwds = {}

        # T_k: width/duration of each block
        if 'T_k' in fitfunc.args:
            kwds['T_k'] = block_length[:R + 1] - block_length[R + 1]

        # N_k: number of elements in each block
        if 'N_k' in fitfunc.args:
            kwds['N_k'] = np.cumsum(weights[:R + 1][::-1])[::-1]

        # evaluate fitness function
        fit_vec = fitfunc.fitness(**kwds)

        A_R = fit_vec - fitfunc.prior(R + 1, N)
        A_R[1:] += best[:R]

        i_max = np.argmax(A_R)
        last[R] = i_max
        best[R] = A_R[i_max]

    # -----------------------------------------------------------------
    # Now find changepoints by iteratively peeling off the last block
    # -----------------------------------------------------------------
    change_points = np.zeros(N, dtype=int)
    i_cp = N
    ind = N
    while True:
        i_cp -= 1
        change_points[i_cp] = ind
        if ind == 0:
            break
        ind = last[ind - 1]
    change_points = change_points[i_cp:]

    return edges[change_points]

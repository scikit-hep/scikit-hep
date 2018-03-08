# Licensed under a 3-clause BSD style license, see LICENSE.
# Brian Pollack, 2017
from __future__ import absolute_import
from __future__ import division
import sys

from skhep.utils.py23 import *

from numbers import Number
from collections import Iterable
import colorsys

import numpy as np

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors, gridspec
import matplotlib.cbook as cbook
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Polygon

import pandas as pd

from skhep.modeling import bayesian_blocks
from skhep.visual.fill_between_steps import fill_between_steps

import warnings
warnings.filterwarnings('ignore')


class MplPlotter(object):
    def __init__(self, show_backend=False):
        if show_backend:
            import matplotlib
            print(matplotlib.get_backend())

    @staticmethod
    def hist(x, bins='auto', range=None, weights=None, errorbars=False, normed=False, scale=None,
             stacked=False, histtype='stepfilled', **kwargs):
        """Enhanced histogram, based on `hist` function from matplotlib and astroML.
        The main additional features are the ability to use data-driven binning algorithms, the
        addition of errorbars, scaling options (like dividing all bin values by their widths), and
        marker-style draw options.  `hist` function wraps `HistContainer` class, which does the
        majority of work.

        Args:
            x (array, or list of array):
                Array of data to be histogrammed.

            bins (int or List or str, optional): If `int`, `bins` number of equal-width bins are
                generated.  The width is determined by either equal divison of the given `range`, or
                equal division between the first and last data point if no `range` is specified.

                If `List`, bin edges are taken directly from `List` (can be unequal width).

                If `str`, then it must be one of::

                        'blocks' : use bayesian blocks for dynamic bin widths.

                        'auto' : use 'auto' feature from numpy.histogram.

                Defaults to 'auto'.

            range (tuple or None, optional): If specificed, data will only be considered and shown
                for the range given.  Otherwise, `range` will be between the highest and lowest
                datapoint.

                Defaults to None.

            weights (array or None, optional): Weights associated with each data point.  If
                specified, bin content will be equal to the sum of all relevant weights.

                Defaults to None.

            errorbars (boolean or array, optional): If True, errorbars will be calculated and
                displayed based on the `err_*` arguments.  The errorbars will be appropriately
                modified if `scale` and/or `normed` is True. If an array is specificed, those values
                will be used (and will not be modifed by any other methods).

                Defaults to False.

            normed (boolean, optional): If True, histogram will be normalized such that the integral
                over all bins with be equal to 1.  In general, this will NOT mean that the sum of
                all bin contents will be 1, unless all bin widths are equal to 1. If used with
                `scale` option, normalization happens before scale.

                Defaults to False

            scale (Number or 'binwidth', optional): If Number, all bin contents are multiplied by
                the given value.  If 'binwidth', every bin content is divided by the bin width. If
                used with `normed` option, scaling occurs after normalization ('binwidth' will be
                ignored in this case, because it is handled automatically when normalizing).

                Defaults to None

            stacked (boolean, optional): If True, multiple input data sets will be layered on top of
                each other, such that the height of each bin is the sum of all the relevant dataset
                contributions.  If used with errorbars, the bars will be associated with the bin
                totals, not the individual components.

                Defaults to False.

            histtype (stepfilled', 'step', 'bar', or 'marker'): Draw options for histograms.
                'stepfilled', 'step', and 'bar' inherit from `matplotlib`.  'marker' places a single
                point at the center of each bin (best used with error bars).  'marker' will throw an
                exception if used with 'stacked' option.

                Defaults to 'stepfilled'.

            **kwargs:
                * ax (matplotlib axes instance):
                    Specify the Axes on which to draw the histogram.  If not specified, then the
                    current active axes will be used, or a new axes instance will be generated.

                    Defaults to current axis.

                * err_style ('band' or 'line'):
                    Draw style for errorbars.

                    Defaults depend on `histtype`,
                    where histtype='stepfilled' corresponds to 'band', and all others correspond to
                    'line'.

                * err_color ('auto' or valid `matplotlib` colors):
                    Color for error bars.  If 'auto' is
                    chosen and `stacked` is False, The color will be a slightly darker version of
                    the associated histogram color.  If `stacked` is True, color will be the next in
                    the current color cycle.

                    Defaults to 'auto'.

                * err_type ('sumW2' or 'gaussian'):
                   Method of calculating error bars, if no error is given.  The 'gaussian' method
                   displays the error of each bin as the square root of the bin content.   The
                   'sumW2' method displays the error as the square of the sum of the squares of the
                   weights.

                   Defaults to 'gaussian' if no weights are given, else 'sumW2'.

                * err_return (bool):
                    Return additional objects corresponding to the values of the error associated
                    with each bin, and the patches used to display the error bars.

                    Defaults to 'False'

            Note:
                Other keyword arguments are described in `pylab.hist()`.

        Returns:
            (bin_content, bin_edges, bin_errors (optional), patches)

            bin_content (array or list of array):
                The values of the histogram bins. See normed or
                density and weights for a description of the possible semantics. If input x is an
                array, then this is an array of length nbins. If input is a sequence arrays [data1,
                data2,..], then this is a list of arrays with the values of the histograms for each
                of the arrays in the same order.

            bin_edges (array):
                The edges of the bins. Length nbins + 1 (nbins left edges and right edge of last
                bin). Always a single array even when multiple data sets are passed in.

            bin_errors (array or list of arrays, optional):
                The values of the error bars associated with each bin.  It is only returned if
                `errorbars` is `True` and `err_return` is True.

            bin_patches (list or list of lists):
                Silent list of individual patches used to create the histogram or list of such list
                if multiple input datasets.


        Brian Pollack, 2017
        """

        # Generate a histogram object

        hist_con = HistContainer(x, bins, range, weights, errorbars, normed, scale, stacked,
                                 histtype, **kwargs)

        if hist_con.err_return:
            return hist_con.bin_content, hist_con.bin_edges, hist_con.bin_err, hist_con.vis_object
        else:
            return hist_con.bin_content, hist_con.bin_edges, hist_con.vis_object

    @staticmethod
    def ratio_plot(hist_dict1, hist_dict2, bins=None, range=None, ratio_range=None,
                   err_style='band', err_color='dimgray', ratio_mode='default', grid=False,
                   unity_line='red', logx=False):
        '''Function for creating ratio plots (comparing two histograms by dividing their bin content).
        The call structure is very similar to producing two individual histograms, with additional
        arguments specifying the nature of the ratio plot.  The number of bins and ranges for both
        histograms must be equal.

        Note:
            Addition documentation soon.'''

        bin_range = range
        del range

        bins, bin_range = _check_args_ratio(hist_dict1, hist_dict2, bins, bin_range)
        hist_dict1['bins'] = bins
        hist_dict1['range'] = bin_range

        fig = plt.figure()
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax1 = fig.add_subplot(gs[0])
        if logx:
            ax1.set_xscale("log", nonposx='clip')
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        # ax1.grid(True)
        # ax2.grid(True)
        plt.setp(ax1.get_xticklabels(), visible=False)
        fig.subplots_adjust(hspace=0.001)

        hist_dict1['ax'] = ax1
        hist_dict2['ax'] = ax1

        hist_con1 = HistContainer(**hist_dict1)
        bin_edges = hist_con1.bin_edges
        bin_range = (bin_edges[0], bin_edges[-1])
        hist_dict2['bins'] = bin_edges
        hist_dict2['range'] = bin_range
        hist_con2 = HistContainer(**hist_dict2)
        ax1.set_xlim(bin_range)

        if hist_con1.stacked:
            bc1 = hist_con1.bin_content[-1]
        else:
            bc1 = hist_con1.bin_content
        if hist_con2.stacked:
            bc2 = hist_con2.bin_content[-1]
        else:
            bc2 = hist_con2.bin_content

        berr1 = getattr(hist_con1, 'bin_err', np.zeros(len(bc1)))
        berr2 = getattr(hist_con2, 'bin_err', np.zeros(len(bc2)))

        ratio = bc1/bc2
        ratio_err = ratio*np.sqrt((berr1/bc1)**2+(berr2/bc2)**2)
        ratio_err_hi = ratio + ratio_err
        ratio_err_low = ratio - ratio_err

        ratio[ratio == 0] = np.nan

        fill_between_steps(ax2, hist_con1.bin_edges, ratio_err_hi, ratio_err_low,
                           step_where='pre', linewidth=0, color=err_color, alpha=0.2, zorder=10)

        ax2.errorbar(hist_con1.bin_centers, ratio, yerr=None,
                     xerr=[hist_con1.bin_centers-hist_con1.bin_edges[0:-1],
                           hist_con1.bin_edges[1:]-hist_con1.bin_centers], fmt='d',
                     color=err_color)

        if unity_line:
            ax2.axhline(1, linewidth=3, color=unity_line, zorder=0)
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=4, prune='upper'))
        if ratio_range:
            ax2.set_ylim(ratio_range)
        else:
            ax2.set_ylim((0, 2.0))

        return (ax1, ax2), (hist_con1.bin_content, hist_con1.bin_edges, hist_con1.vis_object), \
            (hist_con2.bin_content, hist_con2.bin_edges, hist_con2.vis_object)


def _check_args_ratio(hist_dict1, hist_dict2, bins, bin_range):

    # check that 'bins' is not conflicting
    if bins is not None:
        _bins = bins
    elif 'bins' in hist_dict1:
        _bins = hist_dict1['bins']
    elif 'bins' in hist_dict2:
        _bins = hist_dict2['bins']
    else:
        _bins = 'auto'

    if (('bins' in hist_dict1 and hist_dict1['bins'] != _bins) or
            ('bins' in hist_dict2 and hist_dict2['bins'] != _bins)):
        raise KeyError('`bins` arg is inconsistent.  All declared `bins` args must be equal')

    # check that 'range' is not conflicting

    if bin_range is not None:
        _bin_range = bin_range
    elif 'range' in hist_dict1:
        _bin_range = hist_dict1['range']
    elif 'range' in hist_dict2:
        _bin_range = hist_dict2['range']
    else:
        _bin_range = None

    if (('range' in hist_dict1 and hist_dict1['range'] != _bin_range) or
            ('range' in hist_dict2 and hist_dict2['range'] != _bin_range)):
        raise KeyError('`range` arg is inconsistent.  All declared `range` args must be equal')

    return _bins, _bin_range


class HistContainer(object):
    """Class to hold histogram properties and members."""
    def __init__(self, x, bins='auto', range=None, weights=None, errorbars=False, normed=False,
                 scale=None, stacked=False, histtype='stepfilled', **kwargs):

        if weights is None:
            self.has_weights = False
        else:
            self.has_weights = True
        x, weights = self._checks_and_wrangling(x, weights)

        # Prevent hiding of builtins, define members from args
        self.bin_range = range
        del range
        self.bins = bins
        if isinstance(errorbars, Iterable):
            self.bin_err = errorbars
            self.errorbars = 'given'
        elif errorbars:
            self.errorbars = 'calc'
        else:
            self.errorbars = False
        self.normed = normed
        self.scale = scale
        self.stacked = stacked
        self.histtype = histtype
        self._arg_init(kwargs, weights)
        self._df_binning_init(x, weights)
        self.do_redraw = False

        if self.normed:
            self.normalize()
        if self.scale:
            self.rescale(self.scale)

        if self.histtype == 'marker':
            self.vis_object = self.ax.plot(self.bin_centers, self.bin_content, **self.hist_dict)

        elif self.do_redraw and not self.histtype == 'marker':
            self.redraw()

        if self.errorbars:
            self.draw_errorbars()
        if self.logy:
            self.set_log_vals()

    def _checks_and_wrangling(self, x, w):
        # Manage the input data in the same fashion as mpl
        if np.isscalar(x):
            x = [x]

        input_empty = (np.size(x) == 0)

        # Massage 'x' for processing.
        if input_empty:
            x = np.array([[]])
        elif mpl.__version__ < '2.1.0':
            x = cbook._reshape_2D(x)
        else:
            x = cbook._reshape_2D(x, 'x')

        self.n_data_sets = len(x)  # number of datasets

        # We need to do to 'weights' what was done to 'x'
        if w is not None:
            if mpl.__version__ < '2.1.0':
                w = cbook._reshape_2D(w)
            else:
                w = cbook._reshape_2D(w, 'w')

        if w is not None and len(w) != self.n_data_sets:
            raise ValueError('weights should have the same shape as x')

        if w is not None:
            for xi, wi in zip(x, w):
                if wi is not None and len(wi) != len(xi):
                    raise ValueError('weights should have the same shape as x')

        return x, w

    def _arg_init(self, kwargs, w):
        # Break up the kwargs into different chunks depending on the arg, and set various defaults.

        # Scaling by `binwidth` is handled by default during normalization
        if self.normed and self.scale == 'binwidth':
            self.scale = None

        if self.histtype == 'marker' and self.stacked:
            raise ValueError('Do not stack with markers, that would be silly')

        if self.histtype == 'marker' and self.n_data_sets > 1:
            raise ValueError('`marker` histtype does not currently support multiple input datasets')

        if self.histtype == 'barstacked' and not self.stacked:
            self.histtype = 'stepfilled'
            self.stacked = True

        # Get current axis
        self.ax = kwargs.pop('ax', plt.gca())

        # Group arguments into different dicts
        # For error bars:
        self.err_dict = {}
        self.err_dict['errorbars'] = self.errorbars

        if self.histtype in ['stepfilled', 'bar']:
            self.err_dict['err_style'] = kwargs.pop('err_style', 'band')
        else:
            self.err_dict['err_style'] = kwargs.pop('err_style', 'line')

        self.err_dict['err_color'] = kwargs.pop('err_color', 'auto')

        # err_color='auto' is not currently supported in python 2.6 due to matplotlib
        # incompatibilities.  If an error bar color is not defined, then it will be set to black by
        # default.
        if sys.version_info < (2, 7):
            self.err_dict['err_color'] = 'k'

        self.err_dict['suppress_zero'] = kwargs.pop('suppress_zero', False)

        if self.has_weights:
            self.err_dict['err_type'] = kwargs.pop('err_type', 'sumW2')
        else:
            self.err_dict['err_type'] = kwargs.pop('err_type', 'gaussian')

        self.err_dict['err_x'] = kwargs.pop('err_x', True)
        self.err_dict['err_return'] = kwargs.pop('err_return', False)
        self.err_return = self.err_dict['err_return']
        if self.err_return and not self.errorbars:
            raise KeyError('Cannot set `err_return=True` if `errorbars=False`')

        # tweak histogram styles for `band` err_style

        if self.err_dict['err_style'] == 'band' and self.errorbars and not self.stacked:
            if 'edgecolor' not in kwargs:
                kwargs['edgecolor'] = 'k'
            if 'linewidth' not in kwargs:
                kwargs['linewidth'] = 1

        # For data-driven binning
        self.bin_dict = {}
        if isinstance(self.bins, str):
            if 'gamma' in kwargs:
                self.bin_dict['gamma'] = kwargs.pop('gamma')
            if 'p0' in kwargs:
                self.bin_dict['p0'] = kwargs.pop('p0')

        self.hist_dict = kwargs
        if self.histtype != 'marker':
            self.hist_dict['histtype'] = self.histtype

        # set some marker defaults
        if self.histtype == 'marker':
            if 'marker' not in self.hist_dict:
                self.hist_dict['marker'] = 'o'
            if 'linestyle' not in self.hist_dict:
                self.hist_dict['linestyle'] = ''

        if 'alpha' not in self.hist_dict:
            if self.histtype in ['marker', 'step']:
                self.hist_dict['alpha'] = 1
            else:
                self.hist_dict['alpha'] = 0.5

        if 'linewidth' not in self.hist_dict and self.histtype == 'step':
            self.hist_dict['linewidth'] = 2

        self.logy = self.hist_dict.pop('log', False)

    def _df_binning_init(self, data, weights):
        '''Do an initial binning to get bin edges, total hist range, and break each set of data and
        weights into a dataframe (easier to handle errorbar calculation moving forward)'''

        # If bin edges are already determined, than skip initial histogramming
        self.bin_edges = None
        if isinstance(self.bins, Iterable) and not isinstance(self.bins, str):
            self.bin_edges = self.bins
            if self.bin_range is None:
                self.bin_range = (self.bin_edges[0], self.bin_edges[-1])

        # If bin edges need to be determined, there's a few different cases to consider
        else:
            if self.stacked:
                _n_data_sets = 1
                b_data = [np.concatenate(data)]
                if self.has_weights:
                    b_weights = [np.concatenate(weights)]
                else:
                    b_weights = None
            else:
                _n_data_sets = self.n_data_sets
                b_data = data
                b_weights = weights

            if self.bin_range is None:
                xmin = np.inf
                xmax = -np.inf
                for i in range(_n_data_sets):
                    if len(data[i]) > 0:
                        xmin = min(xmin, min(b_data[i]))
                        xmax = max(xmax, max(b_data[i]))
                self.bin_range = (xmin, xmax)

            # Special case for Bayesian Blocks
            if self.bins in ['block', 'blocks']:

                # Single data-set or stacked
                if _n_data_sets == 1:

                    if self.has_weights:
                        b_weights = b_weights[0]
                    else:
                        b_weights = None
                    self.bin_edges = bayesian_blocks(data=b_data[0], weights=b_weights,
                                                     **self.bin_dict)
                else:
                    raise ValueError('Cannot use Bayesian Blocks with multiple, unstacked datasets')

            else:
                _, self.bin_edges = np.histogram(b_data, bins=self.bins, weights=b_weights,
                                                 range=self.bin_range)

        self.widths = np.diff(self.bin_edges)
        self.bin_centers = self.bin_edges[:-1]+self.widths*0.5

        # Now put the data into dataframes with the weights and bins
        self.df_list = []
        for i in range(self.n_data_sets):
            if weights is None:
                df = pd.DataFrame({'data': data[i]})
            else:
                df = pd.DataFrame({'data': data[i], 'weights': weights[i]})
            df_bins = pd.cut(df.data, self.bin_edges, include_lowest=True)
            df['bins'] = df_bins
            self.df_list.append(df)

        # Make the initial histograms
        if self.histtype == 'marker':
            self.bin_content, _ = np.histogram(data, self.bin_edges, weights=weights,
                                               range=self.bin_range)
        else:
            self.bin_content, _, self.vis_object = self.ax.hist(data, self.bin_edges,
                                                                weights=weights,
                                                                range=self.bin_range,
                                                                stacked=self.stacked,
                                                                **self.hist_dict)

            # if self.stacked and self.errorbars and self.histtype == 'stepfilled':
            #     plt.setp(self.vis_object[-1][0], edgecolor='k')
            #     plt.setp(self.vis_object[-1][0], linewidth=2)

        self.bin_content_orig = self.bin_content[:]

        if self.errorbars == 'calc' and not (self.normed or self.scale):
            self.calc_bin_error(hist_mod='default')

    def normalize(self):
        self.do_redraw = True
        data = [df.data for df in self.df_list]
        if self.has_weights:
            weights = [df.weights for df in self.df_list]
            if self.stacked:
                weights = np.concatenate(weights)
        elif self.n_data_sets == 1 or self.stacked:
            weights = None
        else:
            weights = [None for df in self.df_list]

        if self.n_data_sets == 1:
            self.bin_content, _ = np.histogram(data, self.bin_edges, weights=weights,
                                               range=self.bin_range, density=True)
        elif self.stacked:
            total_bin_content, _ = np.histogram(np.concatenate(data), self.bin_edges,
                                                weights=weights, range=self.bin_range, density=True)
            bin_scales = np.divide(total_bin_content, self.bin_content[-1])
            for i in range(self.n_data_sets):
                self.bin_content[i] = np.multiply(bin_scales, self.bin_content[i])

        else:
            self.bin_content = []
            for i, d in enumerate(data):
                self.bin_content.append(np.histogram(d, self.bin_edges, weights=weights[i],
                                                     range=self.bin_range, density=True)[0])

        if self.errorbars == 'calc':
            self.calc_bin_error(hist_mod='norm')

    def rescale(self, scale):
        self.do_redraw = True

        if isinstance(scale, Number):
            self.bin_content = np.multiply(self.bin_content, scale)
            if self.errorbars == 'calc':
                self.calc_bin_error(hist_mod='scale', scale=scale, exist=self.normed)

        elif scale == 'binwidth':
            widths = np.diff(self.bin_edges)
            self.bin_content = np.divide(self.bin_content, widths)
            if self.errorbars == 'calc':
                self.calc_bin_error(hist_mod='scale', scale=1.0/widths, exist=self.normed)

    def calc_bin_error(self, hist_mod='default', scale=None, exist=False):

        # make new error bars if they haven't been calc'd
        if not exist:
            data = [df.data for df in self.df_list]
            if self.stacked:
                data = np.concatenate(data)

            if self.has_weights:
                weights = [df.weights for df in self.df_list]
                if self.stacked:
                    weights = np.concatenate(weights)
            elif self.n_data_sets == 1 or self.stacked:
                weights = None
            else:
                weights = [None for df in self.df_list]

            if self.n_data_sets == 1 or self.stacked:
                bin_content_no_norm, _ = np.histogram(data, self.bin_edges, weights=weights,
                                                      range=self.bin_range)
            else:
                bin_content_no_norm = []
                for i, d in enumerate(data):
                    bin_content_no_norm.append(np.histogram(d, self.bin_edges, weights=weights[i],
                                                            range=self.bin_range)[0])

            if self.err_dict['err_type'] == 'gaussian':
                bin_err_tmp = np.sqrt(bin_content_no_norm)
                # bin_err_tmp = np.sqrt(self.bin_content)

            elif self.err_dict['err_type'] == 'sumW2':
                bin_err_tmp = []
                if self.stacked:
                    # bug in pd.concat for py26 with categorical objects (which are created by
                    # pd.cut, for instance).  This bug is fixed in pandas 0.17.0, but that py26
                    # support was dropped in that version (and subsequent versions).  Solution is
                    # to concatinate the dataframes without the 'bins' column, and then recalculate
                    if sys.version_info < (2, 7):
                        df_list_tmp = [self.df_list[0].drop('bins', axis=1)]
                        for df in self.df_list[1:]:
                            df_list_tmp.append(df.drop('bins', axis=1))
                        df_list_tmp = [pd.concat(df_list_tmp, ignore_index=True)]
                        df_bins = pd.cut(df_list_tmp[0].data, self.bin_edges, include_lowest=True)
                        df_list_tmp[0]['bins'] = df_bins
                    else:
                        df_list_tmp = [pd.concat(self.df_list, ignore_index=True)]
                else:
                    df_list_tmp = self.df_list

                for df in df_list_tmp:
                    df['weights2'] = np.square(df.weights)
                    bin_err_tmp.append(np.sqrt((
                        df.groupby('bins')['weights2'].sum().fillna(0).values)))

                bin_err_tmp = bin_err_tmp[-1]

            elif self.err_dict['err_type'] == 'poisson':
                err_low = np.asarray([poisson_error(bc, self.err_dict['suppress_zero'])[0] for bc
                                      in bin_content_no_norm])
                err_hi = np.asarray([poisson_error(bc, self.err_dict['suppress_zero'])[1] for bc in
                                     bin_content_no_norm])
                bin_err_tmp = np.asarray([err_low, err_hi])

            else:
                raise KeyError('`err_type: {0}` not implemented'.format(self.err_dict['err_type']))

            # Modifiy the error bars if needed (due to normalization or scaling)
            if hist_mod == 'default':
                self.bin_err = bin_err_tmp

            elif hist_mod == 'norm':
                if self.stacked:
                    bc = self.bin_content[-1]
                else:
                    bc = self.bin_content
                self.bin_err = bin_err_tmp*(np.divide(bc, bin_content_no_norm))

            elif hist_mod == 'scale':
                self.bin_err = np.multiply(bin_err_tmp, scale)

        # if errors already exist due to norm calc
        else:
            self.bin_err = np.multiply(self.bin_err, scale)

    def draw_errorbars(self):
        if self.n_data_sets == 1:
            bin_height = [self.bin_content]
            bin_err = [self.bin_err]
            if self.histtype != 'marker':
                vis_object = [self.vis_object]
            else:
                vis_object = self.vis_object
        elif self.stacked:
            bin_height = [self.bin_content[-1]]
            bin_err = [self.bin_err]
            vis_object = [self.vis_object]
        else:
            bin_height = self.bin_content
            bin_err = self.bin_err
            vis_object = self.vis_object

        if not self.stacked:
            n_data_sets_eff = self.n_data_sets
        else:
            n_data_sets_eff = 1
        for i in range(n_data_sets_eff):
            if self.err_dict['err_color'] == 'auto' and not self.stacked:
                if self.histtype == 'marker':
                    err_color = colors.to_rgba(vis_object[i]._get_rgba_face())
                elif self.histtype in ['stepfilled', 'bar']:
                    err_color = colors.to_rgba(vis_object[i][0].get_facecolor())
                elif self.histtype == 'step':
                    err_color = colors.to_rgba(vis_object[i][0].get_edgecolor())

                hls_tmp = colorsys.rgb_to_hls(*err_color[:-1])
                err_color = list(colorsys.hls_to_rgb(hls_tmp[0], hls_tmp[1]*0.7, hls_tmp[2])) + \
                    [err_color[-1]]
            elif self.err_dict['err_color'] == 'auto' and self.stacked:
                err_color = next(self.ax._get_lines.prop_cycler)['color']
            else:
                err_color = self.err_dict['err_color']

            if self.histtype == 'marker':
                if self.err_dict['err_x']:
                    xerr = self.widths*0.5
                else:
                    xerr = None
                _, caps, _ = self.ax.errorbar(self.bin_centers, bin_height[i], linestyle='',
                                              marker='', yerr=bin_err[i], xerr=xerr,
                                              linewidth=2, color=err_color)
            else:
                if self.err_dict['err_style'] == 'line':
                    self.ax.errorbar(self.bin_centers, bin_height[i], linestyle='', marker='',
                                     yerr=bin_err[i], linewidth=2, color=err_color)

                elif self.err_dict['err_style'] == 'band':
                    if self.err_dict['err_type'] == 'poisson':
                        fill_between_steps(self.ax, self.bin_edges, bin_height[i]+bin_err[i][1],
                                           bin_height[i]-bin_err[i][0], step_where='pre',
                                           linewidth=0, color=err_color,
                                           alpha=self.hist_dict['alpha']*0.8, zorder=10)
                    else:
                        fill_between_steps(self.ax, self.bin_edges, bin_height[i]+bin_err[i],
                                           bin_height[i]-bin_err[i], step_where='pre', linewidth=0,
                                           color=err_color, alpha=self.hist_dict['alpha']*0.8,
                                           zorder=10)

                    if self.stacked:
                        poly_patch = self.vis_object[-1][0].get_xy()
                        self.ax.add_patch(Polygon(poly_patch[:(len(poly_patch)+1)//2], closed=False,
                                          facecolor='none', edgecolor='k', linewidth=1, alpha=0.5,
                                                  zorder=0))

    def redraw(self):
        self.bc_scales = np.divide(self.bin_content, self.bin_content_orig)
        self.bc_scales[-1] = np.nan_to_num(self.bc_scales[-1])
        self.do_redraw = False
        if self.n_data_sets == 1:
            bin_content = [self.bin_content]
            if self.histtype != 'marker':
                vis_object = [self.vis_object]
        else:
            bin_content = self.bin_content
            vis_object = self.vis_object

        for n in range(self.n_data_sets):
            if self.stacked:
                xy = vis_object[n][0].get_xy()
                j = 0
                for bcs in self.bc_scales[-1]:
                    xy[j+1, 1] *= bcs
                    xy[j+2, 1] *= bcs
                    j += 2
                if self.histtype == 'step':
                    xy[0, 1] *= self.bc_scales[-1][0]
                    xy[-1, 1] *= self.bc_scales[-1][-1]
                elif self.histtype in ['bar', 'stepfilled']:
                    for bcs in self.bc_scales[-1][::-1]:
                        xy[j+1, 1] *= bcs
                        xy[j+2, 1] *= bcs
                        j += 2
                    xy[0, 1] = xy[-1, 1]
                plt.setp(vis_object[n][0], 'xy', xy)

            else:
                if self.histtype == 'bar':
                    for i, bc in enumerate(bin_content[n]):
                        plt.setp(vis_object[n][i], 'height', bc)
                elif self.histtype == 'stepfilled' or self.histtype == 'step':
                    xy = vis_object[n][0].get_xy()
                    j = 0
                    for bc in bin_content[n]:
                        xy[j+1, 1] = bc
                        xy[j+2, 1] = bc
                        j += 2
                    plt.setp(vis_object[n][0], 'xy', xy)

        self.ax.relim()
        self.ax.autoscale_view(False, False, True)

    def set_log_vals(self):
        self.ax.set_yscale('log', nonposy='clip')
        logbase = self.ax.yaxis._scale.base
        ymin = np.min(self.bin_content[np.nonzero(self.bin_content)])
        self.ax.set_ylim(ymin=min(self.ax.get_ylim()[0], ymin/logbase))


def poisson_error(bin_content, suppress_zero=False):
    '''Returns a high and low 1-sigma error bar for an input bin value, as defined in:
    https://www-cdf.fnal.gov/physics/statistics/notes/pois_eb.txt
    If bin_content > 9, returns the sqrt(bin_content)'''
    error_dict = {
        0: (0.000000, 1.000000),
        1: (0.381966, 2.618034),
        2: (1.000000, 4.000000),
        3: (1.697224, 5.302776),
        4: (2.438447, 6.561553),
        5: (3.208712, 7.791288),
        6: (4.000000, 9.000000),
        7: (4.807418, 10.192582),
        8: (5.627719, 11.372281),
        9: (6.458619, 12.541381)}

    if suppress_zero and bin_content == 0:
        return (0, 0)
    elif bin_content in error_dict:
        return error_dict[bin_content]
    else:
        return (np.sqrt(bin_content), np.sqrt(bin_content))

import os
import sys
import matplotlib as mpl

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import skhep
from skhep.visual import MplPlotter as skh_plt
import pytest

answer_dir = os.path.dirname(skhep.__file__)+'/../tests/data/visual'


def test_plot_object():
    obj = skh_plt(show_backend=True)
    assert(not (isinstance(type(obj), type(None))))


def test_simple_hist1(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0])

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_simple_hist1')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_simple_hist2(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], weights=data_gen[2], bins=20, normed=True,
                          scale='binwidth', color='red', histtype='step')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_simple_hist2')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_simple_hist3(cmdopt, data_gen):
    output = skh_plt.hist(data_gen[0], weights=data_gen[2], bins=range(5), normed=True,
                          scale='binwidth', color='red', histtype='step')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist3.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_simple_hist3')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist3.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_simple_hist4(cmdopt, data_gen):
    output = skh_plt.hist(data_gen[0], weights=data_gen[2], bins=range(5), normed=True,
                          scale='binwidth', color='red', histtype='bar')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist4.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_simple_hist4')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist4.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_blocks_hist(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], bins='blocks', scale='binwidth', color='green')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_blocks_hist.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_blocks_hist')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_blocks_hist.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_blocks_hist2(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], weights=data_gen[2], bins='blocks', scale='binwidth',
                          color='green', p0=0.1)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_blocks_hist2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_blocks_hist2')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_blocks_hist2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))

    with pytest.raises(ValueError):
        skh_plt.hist([data_gen[0], data_gen[1]], bins='blocks', scale='binwidth', color='green',
                     gamma=0.1)


def test_multi_hist1(cmdopt, data_gen):

    output = skh_plt.hist([data_gen[0], data_gen[1]], bins=20, normed=True)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_multi_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.title('test_multi_hist1')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_multi_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_error_bars(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], bins=20, errorbars=True, err_return=True, scale=5)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars2(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], bins=1, errorbars=True, scale=0.5, normed=True,
                          err_color='k', alpha=0.1, err_type='poisson', err_return=True)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars2')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars3(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], bins=20, errorbars=range(20), err_return=True,
                          histtype='step')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars3.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars3')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars3.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars4(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], bins=50, errorbars=True, err_return=True,
                          histtype='step', err_type='poisson', suppress_zero=True, scale='binwidth')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars4.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars4')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars4.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars_weighted(cmdopt, data_gen):

    output = skh_plt.hist(data_gen[0], weights=data_gen[2], bins=20, errorbars=True,
                          err_return=True)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars_weighted.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars_weighted')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars_weighted.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars_multi(cmdopt, data_gen):

    output = skh_plt.hist([data_gen[0], data_gen[1]], bins=20, stacked=False, errorbars=True,
                          err_return=True,)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars_multi.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_multi')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars_multi.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars_stacked(cmdopt, data_gen):

    output = skh_plt.hist([data_gen[0], data_gen[1]], bins=20, stacked=True, errorbars=True,
                          err_return=True)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars_stacked.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars_stacked')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars_stacked.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars_stacked2(cmdopt, data_gen):

    output = skh_plt.hist([data_gen[0], data_gen[1]], bins=20, histtype='barstacked',
                          weights=[data_gen[2], data_gen[2]], errorbars=True, err_return=True,
                          normed=True, scale=2)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars_stacked2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars_stacked2')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars_stacked2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_error_bars_stacked3(cmdopt, data_gen):

    output = skh_plt.hist([data_gen[0], data_gen[1]], bins=20, histtype='step', stacked=True,
                          weights=[data_gen[2], data_gen[2]], errorbars=True, err_return=True,
                          normed=True, scale=2)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_error_bars_stacked3.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1], berr=output[2])
        plt.title('test_error_bars_stacked2')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_error_bars_stacked3.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))
        assert(np.all(output[2] == answers['berr']))


def test_hist_fails(cmdopt, data_gen):
    with pytest.raises(ValueError):
        skh_plt.hist([data_gen[0], data_gen[1]], stacked=True, histtype='marker')
    with pytest.raises(ValueError):
        skh_plt.hist([data_gen[0], data_gen[1]], histtype='marker')
    with pytest.raises(KeyError):
        skh_plt.hist(1, err_return=True)
    with pytest.raises(ValueError):
        skh_plt.hist([data_gen[0], data_gen[1]], weights=data_gen[2])
    with pytest.raises(ValueError):
        skh_plt.hist(data_gen[0], weights=data_gen[2][0:10])
    with pytest.raises(KeyError):
        skh_plt.hist(data_gen[0], err_type='fake', errorbars=True)

    output1 = skh_plt.hist(5)
    assert(np.all(output1[0] == 1))
    if sys.version_info < (2, 7):
        with pytest.raises(ValueError):
            output2 = skh_plt.hist([], range=(0, 1))
    else:
        output2 = skh_plt.hist([], range=(0, 1))
        assert(np.all(output2[0] == 0))


def test_ratio_plot(cmdopt, data_gen):

    output = skh_plt.ratio_plot(dict(x=data_gen[0], errorbars=True, histtype='marker'),
                                dict(x=data_gen[1], weights=data_gen[2], errorbars=True))

    if cmdopt == "generate":
        with open(answer_dir+'/answers_ratio_plot.npz', 'wb') as f:
            np.savez(f, bc1=output[1][0], be1=output[1][1],
                     bc2=output[2][0], be2=output[2][1])
        output[0][0].set_title('test_ratio_plot')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_ratio_plot.npz')
        assert(np.all(output[1][0] == answers['bc1']))
        assert(np.all(output[1][1] == answers['be1']))
        assert(np.all(output[2][0] == answers['bc2']))
        assert(np.all(output[2][1] == answers['be2']))


def test_ratio_plot_stacked(cmdopt, data_gen):

    output = skh_plt.ratio_plot(
        dict(x=[data_gen[0], data_gen[1]], stacked=True, errorbars=True),
        dict(x=[data_gen[0], data_gen[1]], weights=[data_gen[2], data_gen[2]], stacked=True,
             errorbars=True, err_style='line'),
        range=(-5, 5), bins='blocks'
    )

    if cmdopt == "generate":
        with open(answer_dir+'/answers_ratio_plot_stacked.npz', 'wb') as f:
            np.savez(f, bc1=output[1][0], be1=output[1][1],
                     bc2=output[2][0], be2=output[2][1])
        output[0][0].set_title('test_ratio_plot_stacked')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_ratio_plot_stacked.npz')
        assert(np.all(output[1][0] == answers['bc1']))
        assert(np.all(output[1][1] == answers['be1']))
        assert(np.all(output[2][0] == answers['bc2']))
        assert(np.all(output[2][1] == answers['be2']))


def test_ratio_plot_log(cmdopt, data_gen):

    output = skh_plt.ratio_plot(dict(x=data_gen[0], errorbars=True, histtype='marker', log=True,
                                     err_x=False),
                                dict(x=data_gen[1], weights=data_gen[2], errorbars=True),
                                logx=True, ratio_range=(0, 10))

    if cmdopt == "generate":
        with open(answer_dir+'/answers_ratio_plot_log.npz', 'wb') as f:
            np.savez(f, bc1=output[1][0], be1=output[1][1],
                     bc2=output[2][0], be2=output[2][1])
        output[0][0].set_title('test_ratio_plot_log')
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_ratio_plot_log.npz')
        assert(np.all(output[1][0] == answers['bc1']))
        assert(np.all(output[1][1] == answers['be1']))
        assert(np.all(output[2][0] == answers['bc2']))
        assert(np.all(output[2][1] == answers['be2']))


def test_ratio_plot_quick(cmdopt, data_gen):
    # bin tests
    with pytest.raises(KeyError):
        skh_plt.ratio_plot(dict(x=data_gen[0], bins=10), dict(x=data_gen[1], bins=11))
    output = skh_plt.ratio_plot(dict(x=data_gen[0]), dict(x=data_gen[1], bins=11))
    assert(len(output[1][0]) == 11)
    # range tests
    with pytest.raises(KeyError):
        skh_plt.ratio_plot(dict(x=data_gen[0], range=(0, 1)), dict(x=data_gen[1], range=(1, 2)))
    output = skh_plt.ratio_plot(dict(x=data_gen[0], range=(-0.1, 0.1)), dict(x=data_gen[1]))
    assert(output[1][1][0] >= -0.1 and output[1][1][-1] <= 0.1)
    output = skh_plt.ratio_plot(dict(x=data_gen[0]), dict(x=data_gen[1], range=(-0.1, 0.1)))
    assert(output[1][1][0] >= -0.1 and output[1][1][-1] <= 0.1)

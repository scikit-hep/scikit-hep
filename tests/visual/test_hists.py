import os
import matplotlib as mpl

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import skhep
from skhep.visual import MplPlotter as skh_plt

answer_dir = os.path.dirname(skhep.__file__)+'/../tests/data/visual'


def test_simple_hist1(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0])

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_simple_hist2(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0], weights=data_gen1[2], bins=20, normed=True, color='red')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_simple_hist2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_simple_hist2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_blocks_hist(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0], bins='blocks', scale='binwidth', color='green')

    if cmdopt == "generate":
        with open(answer_dir+'/answers_blocks_hist.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_blocks_hist.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_multi_hist1(cmdopt, data_gen1):

    output = skh_plt.hist([data_gen1[0], data_gen1[2]], bins=20, stacked=False, normed=True)

    if cmdopt == "generate":
        with open(answer_dir+'/answers_multi_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_multi_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))

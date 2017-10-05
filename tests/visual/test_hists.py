import os
import numpy as np
import matplotlib.pyplot as plt
import skhep
from skhep.visual import MplPlotter as skh_plt

test_dir = os.path.dirname(skhep.__file__)+'/../tests/visual'


def test_simple_hist1(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0])

    if cmdopt == "generate":
        with open(test_dir+'/answers/answers_simple_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(test_dir+'/answers/answers_simple_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_simple_hist2(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0], weights=data_gen1[2], bins=20, normed=True, color='red')

    if cmdopt == "generate":
        with open(test_dir+'/answers/answers_simple_hist2.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(test_dir+'/answers/answers_simple_hist2.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_blocks_hist(cmdopt, data_gen1):

    output = skh_plt.hist(data_gen1[0], bins='blocks', scale='binwidth', color='green')

    if cmdopt == "generate":
        with open(test_dir+'/answers/answers_blocks_hist.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(test_dir+'/answers/answers_blocks_hist.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))


def test_multi_hist1(cmdopt, data_gen1):

    output = skh_plt.hist([data_gen1[0], data_gen1[2]], bins=20, stacked=False, normed=True)

    if cmdopt == "generate":
        with open(test_dir+'/answers/answers_multi_hist1.npz', 'wb') as f:
            np.savez(f, bc=output[0], be=output[1])
        plt.show()
    elif cmdopt == "test":
        answers = np.load(test_dir+'/answers/answers_multi_hist1.npz')
        assert(np.all(output[0] == answers['bc']))
        assert(np.all(output[1] == answers['be']))

import os
import numpy as np
import skhep
from skhep.modeling import bayesian_blocks

answer_dir = os.path.dirname(skhep.__file__)+'/../tests/data/modeling'


def test_bayesian_blocks(cmdopt, data_gen):

    be1 = bayesian_blocks(data_gen[0], p0=0.05)
    be2 = bayesian_blocks(data_gen[0], gamma=0.1)
    be3 = bayesian_blocks(data_gen[0], weights=data_gen[2])

    if cmdopt == "generate":
        with open(answer_dir+'/answers_bayesian_blocks.npz', 'wb') as f:
            np.savez(f, be1=be1, be2=be2, be3=be3)
    elif cmdopt == "test":
        answers = np.load(answer_dir+'/answers_bayesian_blocks.npz')
        assert(np.all(be1 == answers['be1']))
        assert(np.all(be2 == answers['be2']))
        assert(np.all(be3 == answers['be3']))
        # assert(np.all(output[1] == answers['be']))

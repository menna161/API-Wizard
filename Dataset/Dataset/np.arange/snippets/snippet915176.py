import numpy as np
from scipy import linalg
from scipy.stats import norm as gaussian
import sobol_seq
import pickle
import itertools
import time
from model.model import run_network, get_numparams, net_kws_defaults, run_kws_defaults, nn_activations


def batch_norm(numlayers, fracs=[0, 0.25, 0.5, 0.75], loss_kw={}):
    '\n    Batch norm all 1 is already done\n    Here run for number of batch norm layers = fracs * number of total layers\n    BN layers are kept as late as possible\n    Example: numlayers = 7, frac = 0.5\n        #BN layers = 7*0.5 rounded up = 4\n        7/4 = 1.75, so BN layers should come after layer 1.75, 3.5, 5.25, 7\n        Rounding up gives 2, 4, 6, 7, i.e. apply_bns = [0,1,0,1,0,1,1]\n    '
    states = []
    loss_stats = []
    losses = np.asarray([])
    for frac in fracs:
        if (frac == 1):
            continue
        apply_bns = np.zeros(numlayers)
        if (frac != 0):
            num_bns = int(np.ceil((frac * numlayers)))
            intervals = np.arange((numlayers / num_bns), (numlayers + 0.001), (numlayers / num_bns), dtype='half')
            intervals = np.ceil(intervals).astype('int')
            apply_bns[(intervals - 1)] = 1
        states.append({'apply_bns': [int(x) for x in apply_bns]})
        loss_stats.append(lossfunc(state=states[(- 1)], **loss_kw))
        losses = np.append(losses, loss_stats[(- 1)]['loss'])
        print('State = {0}, Loss = {1}\n'.format(states[(- 1)], losses[(- 1)]))
    (best_pos, best_loss) = (np.argmin(losses), np.min(losses))
    (best_state, best_loss_stats) = (states[best_pos], loss_stats[best_pos])
    print('\nBest state = {0}, Best loss = {1}'.format(best_state, best_loss))
    return (best_state, best_loss, best_loss_stats)

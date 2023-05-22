import numpy as np
from scipy import linalg
from scipy.stats import norm as gaussian
import sobol_seq
import pickle
import itertools
import time
from model.model import run_network, get_numparams, net_kws_defaults, run_kws_defaults, nn_activations


def dropout(numlayers, fracs=[0, 0.25, 0.5, 0.75, 1], input_drop_probs=[0.1, 0.2], drop_probs=[0.15, 0.3, 0.45], loss_kw={}, done_state={}):
    "\n    Same logic as batch_norm, i.e. distribute frac number of dropout layers evenly (as late as possible for fractions)\n    For each dropout config, all intermediate layer drop probs are kept to p which varies in drop_probs\n    If input layer dropout is present, its keep prob p varies in input_drop_probs\n    done_state is any state which has already been tested, example for numlayers = 4, done_state could be {'apply_dropouts':[1,1,1,1], 'dropout_probs':[0.1,0.3,0.3,0.3]}\n    "
    states = []
    loss_stats = []
    losses = np.asarray([])
    for frac in fracs:
        apply_dropouts = np.zeros(numlayers)
        dropout_probs = []
        if (frac == 0):
            states.append({'apply_dropouts': [int(x) for x in apply_dropouts], 'dropout_probs': dropout_probs})
        else:
            num_dropouts = int(np.ceil((frac * numlayers)))
            intervals = np.arange((numlayers / num_dropouts), (numlayers + 0.001), (numlayers / num_dropouts), dtype='half')
            intervals = np.ceil(intervals).astype('int')
            apply_dropouts[(intervals - 1)] = 1
            for drop_prob in drop_probs:
                if (apply_dropouts[0] != 1):
                    dropout_probs = (num_dropouts * [drop_prob])
                    states.append({'apply_dropouts': [int(x) for x in apply_dropouts], 'dropout_probs': dropout_probs})
                else:
                    for input_drop_prob in input_drop_probs:
                        dropout_probs = [*[input_drop_prob], *((num_dropouts - 1) * [drop_prob])]
                        states.append({'apply_dropouts': [int(x) for x in apply_dropouts], 'dropout_probs': dropout_probs})
    for (i, state) in enumerate(states):
        if ((list(state['apply_dropouts']) == list(done_state['apply_dropouts'])) and (list(state['dropout_probs']) == list(done_state['dropout_probs']))):
            del states[i]
    for state in states:
        loss_stats.append(lossfunc(state=state, **loss_kw))
        losses = np.append(losses, loss_stats[(- 1)]['loss'])
        print('State = {0}, Loss = {1}\n'.format(state, losses[(- 1)]))
    (best_pos, best_loss) = (np.argmin(losses), np.min(losses))
    (best_state, best_loss_stats) = (states[best_pos], loss_stats[best_pos])
    print('\nBest state = {0}, Best loss = {1}'.format(best_state, best_loss))
    return (best_state, best_loss, best_loss_stats)

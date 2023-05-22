import numpy as np
from scipy import linalg
from scipy.stats import norm as gaussian
import sobol_seq
import pickle
import itertools
import time
from model.model import run_network, get_numparams, net_kws_defaults, run_kws_defaults, nn_activations


def bayesopt(state_kw={}, loss_kw={}, mu_val=None, covmat_kw={}, cov_keys=[], omega={}, kernel_comb_weights={}, noise_var=0.0001, steps=20, initial_states_size=10, new_states_size=100, ksi=0.0001, num_best=1):
    '\n    state_kw : kwargs for get_state()\n    loss_kw : kwargs for lossfunc()\n    mu_val : If None, always normalize values to get mu for all. Otherwise make mu for all equal to this\n    covmat_kw : kwargs for covmat. Do NOT omit any kwargs here since these are pased as args when calling minimize()\n    \n    steps : #steps in BO\n    initial_states_size : #prior points to form initial approximation\n    new_states_size : #points for which to calculate acquisition function in each step\n    ksi : As in ei()\n    \n    num_best : Return this many best states, e.g. top 3\n    '
    print('{0} initial states:'.format(initial_states_size))
    states = get_states(numstates=initial_states_size, samp='sobol', **state_kw)
    loss_stats = []
    losses = np.asarray([])
    for (i, state) in enumerate(states):
        loss_stats.append(lossfunc(state=state, **loss_kw))
        losses = np.append(losses, loss_stats[(- 1)]['loss'])
        print('State {0} = {1}, Loss = {2}\n'.format((i + 1), state, losses[(- 1)]))
    print('Optimization starts:')
    cov_keys = (convert_keys(states[0].keys()) if (cov_keys == []) else cov_keys)
    omega = ({key: 3 for key in cov_keys} if (omega == {}) else omega)
    kernel_comb_weights = ({key: 1 for key in cov_keys} if (kernel_comb_weights == {}) else kernel_comb_weights)
    covmat_kw.update({'cov_keys': cov_keys, 'omega': omega, 'kernel_comb_weights': kernel_comb_weights})
    for step in range(steps):
        mu_val = (np.mean(losses) if (mu_val == None) else mu_val)
        mu = (mu_val * np.ones(len(losses)))
        K = covmat(S1=states, S2=states, **covmat_kw)
        K_inv = linalg.inv((K + (noise_var * np.eye(K.shape[0]))))
        norm_losses = (losses - mu)
        new_states = get_states(numstates=new_states_size, samp='random', **state_kw)
        eis = np.zeros(len(new_states))
        for i in range(len(new_states)):
            (post_mu, post_var) = gp_predict(new_S=new_states[i:(i + 1)], S=states, mu_val=mu_val, norm_Y=norm_losses, K_inv=K_inv, **covmat_kw)
            eis[i] = ei(post_mu=post_mu.flatten()[0], post_std=np.sqrt(post_var.flatten()[0]), best_Y=np.min(losses), ksi=ksi)
        best_state = new_states[np.argmax(eis)]
        states.append(best_state)
        loss_stats.append(lossfunc(state=best_state, **loss_kw))
        losses = np.append(losses, loss_stats[(- 1)]['loss'])
        print('Step {0}, Best State = {1}, Loss = {2}\n'.format((step + 1), best_state, losses[(- 1)]))
    poses = np.argsort(losses)
    best_states = [states[pos] for pos in poses[:num_best]]
    best_loss_stats = [loss_stats[pos] for pos in poses[:num_best]]
    for (i, bs) in enumerate(best_states):
        print('#{0}: Best state = {1}, Corresponding stats = {2}'.format((i + 1), bs, best_loss_stats[i]))
    return (best_states, best_loss_stats)

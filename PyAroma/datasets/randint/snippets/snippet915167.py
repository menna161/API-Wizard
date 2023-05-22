import numpy as np
from scipy import linalg
from scipy.stats import norm as gaussian
import sobol_seq
import pickle
import itertools
import time
from model.model import run_network, get_numparams, net_kws_defaults, run_kws_defaults, nn_activations


def get_states(numstates=15, state_keys=['out_channels'], samp='sobol', nsv=20, limits={'num_conv_layers': (4, 8), 'out_channels_first': (16, 64), 'out_channels': (0, 512), 'num_hidden_layers_mlp': (0, 3), 'hidden_nodes_mlp': (50, 1000), 'lr': ((- 5), (- 1)), 'weight_decay': ((- 6), (- 3)), 'batch_size': (32, 512)}):
    "\n    *** Generate a number of states ***\n    numstates: How many states to generate\n    state_keys: Each state is a dict with these keys, i.e. these form the current search space\n    samp: 'sobol' to use Sobol sampling, 'random' to use random sampling\n    nsv: Number of sampling vectors. Each vector is unique. Ideally this should be greater than number of keys, but even if not, vectors are repeated cyclically\n        Eg: Say search space has out_channels and max num_conv_layers is 10. Then nsv should ideally be >=10\n    limits: Limits for different state_keys. Keys may not match those in state_keys\n        out_channels lower limit is a dummy. Upper limit is important    \n        lr limits are log10(lr)\n        weight_decay limits are log10(wd), and the last power of 10 is converted to actual weight_decay = 0\n    "
    states = [{key: [] for key in state_keys} for _ in range(numstates)]
    if (samp == 'sobol'):
        samp = sobol_seq.i4_sobol_generate(nsv, numstates)
    elif (samp == 'random'):
        samp = np.random.rand(numstates, nsv)
    si = np.random.randint(nsv)
    if ('out_channels' in state_keys):
        (lower, upper) = limits['num_conv_layers']
        num_conv_layers = (lower + (samp[(:, (si % nsv))] * ((upper + 1) - lower))).astype('int')
        si += 1
        (lower, upper) = limits['out_channels_first']
        out_channels_first = (lower + (samp[(:, (si % nsv))] * ((upper + 1) - lower))).astype('int')
        for n in range(numstates):
            states[n]['out_channels'] = (num_conv_layers[n] * [0])
            states[n]['out_channels'][0] = out_channels_first[n]
            states[n]['apply_maxpools'] = (num_conv_layers[n] * [0])
            count_maxpools = 0
            for i in range(1, num_conv_layers[n]):
                lower = states[n]['out_channels'][(i - 1)]
                upper = np.minimum((2 * states[n]['out_channels'][(i - 1)]), limits['out_channels'][1])
                states[n]['out_channels'][i] = (lower + (samp[(n, ((si + i) % nsv))] * ((upper + 1) - lower))).astype('int')
                if ((states[n]['out_channels'][i] > 64) and (count_maxpools == 0)):
                    states[n]['apply_maxpools'][(i - 1)] = 1
                    count_maxpools += 1
                elif ((states[n]['out_channels'][i] > 128) and (count_maxpools == 1)):
                    states[n]['apply_maxpools'][(i - 1)] = 1
                    count_maxpools += 1
                elif ((states[n]['out_channels'][i] > 256) and (count_maxpools == 2)):
                    states[n]['apply_maxpools'][(i - 1)] = 1
                    count_maxpools += 1
            states[n]['shortcuts'] = form_shortcuts(num_conv_layers[n], start_every=form_shortcuts_start_every(num_conv_layers[n]))
        si += limits['num_conv_layers'][1]
    if ('hidden_mlp' in state_keys):
        (lower, upper) = limits['num_hidden_layers_mlp']
        num_hidden_layers_mlp = (lower + (samp[(:, (si % nsv))] * ((upper + 1) - lower))).astype('int')
        si += 1
        (lower, upper) = limits['hidden_nodes_mlp']
        hidden_mlps = []
        for _ in range(limits['num_hidden_layers_mlp'][1]):
            hidden_mlps.append((lower + (samp[(:, (si % nsv))] * ((upper + 1) - lower))).astype('int'))
            si += 1
        hidden_mlps = np.asarray(hidden_mlps)
        for n in range(numstates):
            states[n]['hidden_mlp'] = list(hidden_mlps[(:num_hidden_layers_mlp[n], n)])
    if ('lr' in state_keys):
        (lower, upper) = limits['lr']
        lrs = (10 ** (lower + (samp[(:, (si % nsv))] * (upper - lower))))
        si += 1
        for n in range(numstates):
            states[n]['lr'] = lrs[n]
    if ('weight_decay' in state_keys):
        (lower, upper) = limits['weight_decay']
        weight_decays = (10 ** (lower + (samp[(:, (si % nsv))] * (upper - lower))))
        si += 1
        weight_decays[(weight_decays < (10 ** (lower + 1)))] = 0.0
        for n in range(numstates):
            states[n]['weight_decay'] = weight_decays[n]
    if ('batch_size' in state_keys):
        (lower, upper) = limits['batch_size']
        batch_sizes = (lower + (samp[(:, (si % nsv))] * ((upper + 1) - lower))).astype(int)
        si += 1
        for n in range(numstates):
            states[n]['batch_size'] = batch_sizes[n].item()
    return states

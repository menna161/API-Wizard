import numpy as np
from scipy import linalg
from scipy.stats import norm as gaussian
import sobol_seq
import pickle
import itertools
import time
from model.model import run_network, get_numparams, net_kws_defaults, run_kws_defaults, nn_activations


def lossfunc(state, net_kw_const={}, run_kw_const={}, validate=True, val_patience=np.inf, test=False, numepochs=100, dataset_code='T', run_network_kw={}, penalize='t_epoch', wc=0.1, tbar_epoch=1, numparams_bar=4000000.0, problem_type='classification'):
    "\n    *** Wrapper function for run_network. Given a net, find its model search loss and other statistics ***\n    \n    Net is described using:\n        state : Params being optimized over\n        net_kw_const, run_kw_const : Params not being optimized over\n    These combine to form net_kw and run_kw for run_network\n        \n    Parameters of run_network which might change according to lossfunc are described using:\n        validate, val_patience, test, numepochs\n        \n    Other parameters of run_network which are not expected to change are given in run_network_kw\n        Example: data, input_size, output_size, num_workers, pin_memory, wt_init, bias_init, verbose\n        \n    penalize: Either 't_epoch' or 'numparams' (CNNs only support t_epoch)\n    wc : weightage given to complexity term\n    tbar_epoch : used to normalize training time\n    numparams_bar: Used to normalize number of parameters\n    \n    Returns: loss_stats dictionary. Most important key is 'loss', which gives model search loss\n    "
    net_kw = {**net_kw_const, **{key: state[key] for key in state.keys() if (key in net_kws_defaults)}}
    run_kw = {**run_kw_const, **{key: state[key] for key in state.keys() if (key in run_kws_defaults)}}
    if ('weight_decay' not in state.keys()):
        run_kw['weight_decay'] = default_weight_decay(dataset_code=dataset_code, input_size=run_network_kw['input_size'], output_size=run_network_kw['output_size'], net_kw=net_kw)
    (net, recs) = run_network(net_kw=net_kw, run_kw=run_kw, validate=validate, val_patience=val_patience, test=test, numepochs=numepochs, **run_network_kw)
    numparams = get_numparams(input_size=run_network_kw['input_size'], output_size=run_network_kw['output_size'], net_kw=net_kw)
    loss_stats = {}
    if (problem_type == 'classification'):
        (acc, ep) = (np.max(recs['val_accs']), (np.argmax(recs['val_accs']) + 1))
        fp = ((100 - acc) / 100.0)
        loss_stats['best_val_acc'] = np.max(recs['val_accs'])
    elif (problem_type == 'regression'):
        (loss, ep) = (np.min(recs['val_losses']), (np.argmin(recs['val_losses']) + 1))
        scale = 10
        fp = (loss * scale)
        loss_stats['best_val_loss'] = np.min(recs['val_losses'])
    fc = ((recs['t_epoch'] / tbar_epoch) if (penalize == 't_epoch') else (numparams / numparams_bar))
    loss_stats['loss'] = np.log10((fp + (wc * fc)))
    loss_stats['t_epoch'] = recs['t_epoch']
    loss_stats['numparams'] = numparams
    return loss_stats

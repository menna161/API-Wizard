import numpy as np
import matplotlib
from matplotlib import pyplot as plt, tri as tri
from matplotlib.ticker import LogLocator, MaxNLocator
from skopt import plots as skopt_plots
import plotly.plotly as plotlypy
import plotly.tools as tls
from utils import check_parameter_count_for_sample, partial_dependence_valid_samples_allow_paramcounts


def plot_param_count(optimizer, result):
    all_dim_values = result.x_iters
    losses = result.func_vals
    par_cnt_scheme = optimizer.adapt_param['par_cnt_scheme']
    param_thr = optimizer.adapt_param['param_thr']
    all_par_dicts = []
    bad_param_cnt_inds = []
    bad_param_dict = []
    for (ind, dim_values) in enumerate(all_dim_values):
        (_, par_dict) = check_parameter_count_for_sample(dim_values, optimizer.hyper_param_names, param_thr, par_cnt_scheme=par_cnt_scheme)
        all_par_dicts.append(par_dict)
        if ((par_dict['total'] < (param_thr * 0.95)) or (par_dict['total'] > param_thr)):
            bad_param_cnt_inds.append(ind)
            bad_param_dict.append(par_dict)
    sorted_inds = np.argsort(losses)
    sorted_losses = [losses[ind] for ind in sorted_inds]
    sorted_par_dicts = [all_par_dicts[ind] for ind in sorted_inds]
    cnn_cnts = np.array([par_dict['cnn'] for par_dict in sorted_par_dicts])
    lstm_cnts = np.array([par_dict['lstm'] for par_dict in sorted_par_dicts])
    ff_cnts = np.array([par_dict['ff'] for par_dict in sorted_par_dicts])
    n_exps = len(sorted_losses)
    exps_range = np.arange(n_exps)
    font = {'size': 16}
    matplotlib.rc('font', **font)
    mpl_fig = plt.figure()
    ax_loss = mpl_fig.add_subplot(211)
    ax_loss.scatter(exps_range, sorted_losses)
    ax_loss.set_ylabel('Validation loss')
    ax = mpl_fig.add_subplot(212, sharex=ax_loss)
    width = 0.5
    p1 = ax.bar(exps_range, cnn_cnts, width)
    p2 = ax.bar(exps_range, lstm_cnts, width, bottom=cnn_cnts)
    p3 = ax.bar(exps_range, ff_cnts, width, bottom=(lstm_cnts + cnn_cnts))
    ax.legend(['CNN', 'LSTM', 'FC'], loc='upper right')
    ax.set_ylabel('Trainable parameter count (in millions)')
    ax.set_xlabel('Experiments ordered by loss')
    y_ticks = np.arange(0, param_thr, 2000000.0)
    y_tickslabels = np.arange(0, (param_thr / 1000000.0), (2000000.0 / 1000000.0))
    y_tickslabels = [str(lab) for lab in y_tickslabels]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tickslabels)
    tmp = [ind for (ind, loss) in enumerate(sorted_losses) if (loss >= 0.17)]
    ax_loss.axvline((tmp[0] - 0.5), linestyle='-', lw=1)
    ax.axvline((tmp[0] - 0.5), linestyle='-', lw=1)

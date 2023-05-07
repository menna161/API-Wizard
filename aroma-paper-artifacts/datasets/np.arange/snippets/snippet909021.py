import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_lockdown_state_daily(ax, stats_lock, x_tick=10):
    n_day_arg = stats_lock.shape[1]
    plot_color = '#3F88C5'
    name_state = 'Lockdown state measure'
    stats_mean_arg = np.mean(stats_lock, axis=0)
    stats_err_arg = stats.sem(stats_lock, axis=0)
    serie = [stats_mean_arg[i] for i in range(n_day_arg)]
    err = [stats_err_arg[i] for i in range(n_day_arg)]
    indices = np.arange(n_day_arg)
    p = ax.errorbar(indices, serie, yerr=err, ecolor='#808080', color=plot_color)
    ax.set_ylabel(name_state)
    ax.set_xlabel('Days since innoculation')
    ax.set_title(('Lockdown evolution : Total area %.2f units' % sum(stats_mean_arg)))
    max_s = int(max(serie))
    min_s = int(min(serie))
    ax.set_xticks(np.arange(0, (int((n_day_arg / x_tick)) * x_tick), int((n_day_arg / x_tick))))
    ax.set_xticklabels(tuple([str(int(((i * n_day_arg) / x_tick))) for i in range(x_tick)]))
    ax.set_yticks(np.arange((min_s - 1), (max_s + 1), (1 + int(((max_s - min_s) / 10)))))
    ax.legend((p[0],), (name_state,))

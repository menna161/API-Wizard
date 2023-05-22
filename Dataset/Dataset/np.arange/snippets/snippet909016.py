import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_r0(ax, stats_r0, lib, x_tick=10):
    n_day_arg = stats_r0.shape[1]
    plot_color = '#3F88C5'
    name_state = lib
    stats_mean_arg = np.mean(stats_r0, axis=0)
    stats_err_arg = stats.sem(stats_r0, axis=0)
    serie = [stats_mean_arg[i] for i in range(n_day_arg)]
    err = [stats_err_arg[i] for i in range(n_day_arg)]
    indices = np.arange(n_day_arg)
    p = ax.errorbar(indices, serie, yerr=err, ecolor='#808080', color=plot_color, linewidth=1.3)
    cst_1 = ax.plot(indices, [1 for _ in range(len(indices))], color='#DC143C')
    ax.set_ylabel(name_state)
    ax.set_xlabel('Days since innoculation')
    ax.set_title('Basic reproduction number evolution')
    max_s = int(max(serie))
    min_s = int(min(serie))
    ax.set_xticks(np.arange(0, (int((n_day_arg / x_tick)) * x_tick), int((n_day_arg / x_tick))))
    ax.set_xticklabels(tuple([str(int(((i * n_day_arg) / x_tick))) for i in range(x_tick)]))
    ax.set_yticks(np.arange(min_s, (math.ceil(max_s) + 1), 0.25))
    ax.legend((p[0], cst_1[0]), (name_state, 'Equilibrium'))

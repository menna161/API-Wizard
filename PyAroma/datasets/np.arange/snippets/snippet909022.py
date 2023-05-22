import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_new_daily_cases(ax, stats_arg, x_tick=10):
    n_day_arg = stats_arg['new'].shape[1]
    stats_mean_arg = np.mean(stats_arg['new'], axis=0)
    stats_err_arg = stats.sem(stats_arg['new'], axis=0)
    new_cases_serie = [stats_mean_arg[i] for i in range(n_day_arg)]
    err = [stats_err_arg[i] for i in range(n_day_arg)]
    indices = np.arange(n_day_arg)
    width = 0.6
    p1 = ax.bar(indices, new_cases_serie, width, yerr=err, align='center', alpha=0.5, ecolor='#808080', color='#44A1A0')
    ax.set_ylabel('New cases')
    ax.set_xlabel('Days since innoculation')
    ax.set_title('New infected cases evolution')
    ax.set_xticks(np.arange(0, (int((n_day_arg / x_tick)) * x_tick), int((n_day_arg / x_tick))))
    ax.set_xticklabels(tuple([str(int(((i * n_day_arg) / x_tick))) for i in range(x_tick)]))
    ax.set_yticks(np.arange(0, int((1 + (max(new_cases_serie) * 1.1))), int((1 + (max(new_cases_serie) / 10)))))
    ax.legend((p1[0],), ('New cases',))

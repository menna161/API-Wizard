import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_specific_population_state_daily(ax, stats_arg, x_tick=10, style='P'):
    n_day_arg = stats_arg['hea'].shape[1]
    type_state = 'hea'
    plot_color = '#3F88C5'
    name_state = 'Healthy'
    if (style == 'I'):
        type_state = 'iso'
        plot_color = '#A63D40'
        name_state = 'Infected'
    if (style == 'P'):
        type_state = 'hos'
        plot_color = '#5000FA'
        name_state = 'Hospitalized'
    if (style == 'D'):
        type_state = 'dea'
        plot_color = '#151515'
        name_state = 'Dead'
    if (style == 'M'):
        type_state = 'imm'
        plot_color = '#90A959'
        name_state = 'Immune'
    stats_mean_arg = {k: np.mean(v, axis=0) for (k, v) in stats_arg.items()}
    stats_err_arg = {k: stats.sem(v, axis=0) for (k, v) in stats_arg.items()}
    serie = [stats_mean_arg[type_state][i] for i in range(n_day_arg)]
    err = [stats_err_arg[type_state][i] for i in range(n_day_arg)]
    indices = np.arange(n_day_arg)
    width = 0.6
    p = ax.bar(indices, serie, width, yerr=err, align='center', alpha=0.5, ecolor='#808080', color=plot_color)
    ax.set_ylabel((name_state + ' population'))
    ax.set_xlabel('Days since innoculation')
    ax.set_title('Pandemic evolution')
    ax.set_xticks(np.arange(0, (int((n_day_arg / x_tick)) * x_tick), int((n_day_arg / x_tick))))
    ax.set_xticklabels(tuple([str(int(((i * n_day_arg) / x_tick))) for i in range(x_tick)]))
    ax.set_yticks(np.arange(0, int((max(serie) * 1.1)), int((1 + (max(serie) / 10)))))
    ax.legend((p[0],), (name_state,))

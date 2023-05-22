import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_meta_simulation(ax, death_stat_arg):
    n_variant_arg = death_stat_arg['dea'].shape[1]
    stats_mean_arg = np.mean(death_stat_arg['dea'], axis=0)
    stats_err_arg = stats.sem(death_stat_arg['dea'], axis=0)
    death_serie = [stats_mean_arg[i] for i in range(n_variant_arg)]
    err = [stats_err_arg[i] for i in range(n_variant_arg)]
    indices = np.arange(n_variant_arg)
    width = 0.6
    p1 = ax.bar(indices, death_serie, width, yerr=err, align='center', alpha=0.5, ecolor='#808080', color='#44A1A0')
    bottom_y = int((min(death_serie) * 0.8))
    top_y = int((1 + (max(death_serie) * 1.2)))
    ax.set_ylim(bottom=bottom_y, top=top_y)
    ax.set_ylabel('Total death')
    ax.set_xlabel('Variant parameter')
    ax.set_title('Total death / covid-19 variant type')
    ax.set_xticks(np.arange(0, n_variant_arg, 1))
    ax.set_xticklabels([round(s, 2) for s in np.arange(0.25, 1.75, (1.5 / n_variant_arg))])
    ax.set_yticks(np.arange(bottom_y, top_y, int((1 + (max(death_serie) / 10)))))
    ax.legend((p1[0],), ('Death',))

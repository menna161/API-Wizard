import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_summary(stats_arg, show_plot, x_tick=10):
    (fig, (ax1, ax2, ax3)) = plt.subplots(3, 1, figsize=(16, 10))
    set_ax_mean_population_state_daily(ax1, stats_arg, x_tick)
    set_ax_new_daily_cases(ax2, stats_arg, x_tick)
    set_ax_specific_population_state_daily(ax3, stats_arg, x_tick)
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax2.set_title('')
    ax3.set_title('')
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-summ-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

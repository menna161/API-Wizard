import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_r0_daily_evolution(stats_arg, show_plot, x_tick=10):
    (fig, ax) = plt.subplots(figsize=(15, 10))
    set_ax_r0(ax, stats_arg['R0d'], 'R0 Daily', x_tick=10)
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-R0-daily-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

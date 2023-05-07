import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_lockdown_state_daily(stats_arg, show_plot, x_tick=10):
    (fig, ax) = plt.subplots(figsize=(15, 10))
    set_ax_lockdown_state_daily(ax, stats_arg['loc'], x_tick)
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-lock-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

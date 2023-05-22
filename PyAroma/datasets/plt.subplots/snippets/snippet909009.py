import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_new_daily_cases(stats_arg, show_plot, x_tick=10):
    (fig, ax) = plt.subplots(figsize=(15, 10))
    set_ax_new_daily_cases(ax, stats_arg, x_tick)
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-new-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

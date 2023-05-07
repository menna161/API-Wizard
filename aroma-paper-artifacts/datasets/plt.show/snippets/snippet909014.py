import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_r0_evolution(stats_arg, show_plot, window_size=3, x_tick=10):
    (fig, ax) = plt.subplots(figsize=(15, 10))
    slid_new = np.array([np.convolve(sn, np.ones(window_size, dtype=int), 'valid') for sn in stats_arg['new']])
    slid_con = np.array([rolling_max(sc, window_size) for sc in (1 + stats_arg['con'])])
    set_ax_r0(ax, (slid_new / slid_con), '2 weeks sliding R0', x_tick=10)
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-R0-evo-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

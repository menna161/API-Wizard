import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_meta_simulation(death_stat_arg, show_plot):
    (fig, ax) = plt.subplots(figsize=(15, 10))
    set_ax_meta_simulation(ax, death_stat_arg)
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-meta-%d-%d.png' % (ts, death_stat_arg['dea'].shape[0], np.max(death_stat_arg['dea']))))

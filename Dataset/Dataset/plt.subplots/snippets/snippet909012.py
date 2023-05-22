import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def draw_examples(stats_arg, show_plot, x_tick=10):
    grid_size = 3
    (fig, axes) = plt.subplots(grid_size, grid_size, figsize=(16, 10))
    if ((grid_size * grid_size) > stats_arg['hea'].shape[0]):
        raise AssertionError('Raise the number of runs (--nrun parameter) to draw examples')
    kmeans = KMeans(n_clusters=(grid_size * grid_size), random_state=0)
    kmeans.fit(stats_arg['hea'][(:, :)])
    (chosen_runs, _) = pairwise_distances_argmin_min(kmeans.cluster_centers_, stats_arg['hea'][(:, :)])
    run_index = 0
    for axes_row in axes:
        for ax in axes_row:
            run_id = chosen_runs[run_index]
            death_pct = ((100 * stats_arg['dea'][run_id][:][(- 1)]) / np.max(stats_arg['hea']))
            set_ax_run_population_state_daily(ax, stats_arg, run_id, x_tick)
            if (run_index != (grid_size - 1)):
                ax.legend('')
            if (run_index != (2 * grid_size)):
                ax.set_xlabel('')
                ax.set_ylabel('')
            ax.set_title(('Run n°%d - Death percentage %.2f %%' % (run_id, death_pct)))
            run_index += 1
    if show_plot:
        plt.show()
    else:
        plt.savefig(('images/output/%d-examples-%d-%d.png' % (ts, stats_arg['hea'].shape[0], np.max(stats_arg['hea']))))

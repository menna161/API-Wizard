import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def set_ax_population_state_daily(ax, stats_arg, x_tick=10):
    n_day_arg = stats_arg['hea'].shape[0]
    n_individual_arg = (1.1 * np.max(stats_arg['hea']))
    dead_serie = [stats_arg['dea'][i] for i in range(n_day_arg)]
    healthy_serie = [stats_arg['hea'][i] for i in range(n_day_arg)]
    infected_serie = [stats_arg['inf'][i] for i in range(n_day_arg)]
    infected_serie_stacked = [(stats_arg['hea'][i] + stats_arg['dea'][i]) for i in range(n_day_arg)]
    hospital_serie = [stats_arg['hos'][i] for i in range(n_day_arg)]
    hospital_serie_stacked = [((stats_arg['hea'][i] + stats_arg['dea'][i]) + stats_arg['inf'][i]) for i in range(n_day_arg)]
    immune_serie = [stats_arg['imm'][i] for i in range(n_day_arg)]
    immune_serie_stacked = [(((stats_arg['hea'][i] + stats_arg['dea'][i]) + stats_arg['inf'][i]) + stats_arg['hos'][i]) for i in range(n_day_arg)]
    isolated_serie = [stats_arg['iso'][i] for i in range(n_day_arg)]
    isolated_serie_stacked = [((((stats_arg['hea'][i] + stats_arg['dea'][i]) + stats_arg['inf'][i]) + stats_arg['imm'][i]) + stats_arg['hos'][i]) for i in range(n_day_arg)]
    indices = np.arange(n_day_arg)
    width = 0.7
    p1 = ax.bar(indices, dead_serie, width, color='#151515')
    p2 = ax.bar(indices, healthy_serie, width, bottom=dead_serie, color='#3F88C5')
    p3 = ax.bar(indices, infected_serie, width, bottom=infected_serie_stacked, color='#A63D40')
    p4 = ax.bar(indices, hospital_serie, width, bottom=hospital_serie_stacked, color='#5000FA')
    p5 = ax.bar(indices, immune_serie, width, bottom=immune_serie_stacked, color='#90A959')
    p6 = ax.bar(indices, isolated_serie, width, bottom=isolated_serie_stacked, color='#008080')
    ax.set_ylabel('Total population')
    ax.set_xlabel('Days since innoculation')
    ax.set_title(('Average pandemic evolution - Death percentage %.2f %%"' % ((100 * dead_serie[(- 1)]) / np.max(stats_arg['hea']))))
    ax.set_xticks(np.arange(0, (int((n_day_arg / x_tick)) * x_tick), int((n_day_arg / x_tick))))
    ax.set_xticklabels(tuple([str(int(((i * n_day_arg) / x_tick))) for i in range(x_tick)]))
    ax.set_yticks(np.arange(0, n_individual_arg, (n_individual_arg / 15)))
    ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), ('Dead', 'Healthy', 'Infected', 'Hospitalized', 'Immune', 'Isolated'), framealpha=0.35, loc='upper right')

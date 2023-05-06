from matplotlib import pyplot as plt
import numpy as np
import torch
import os
import yaml
import math
import argparse


def plot_hyperparam(ax, alg, param):
    relevant_dict = relevant_param(alg)
    hyperparam_range = relevant_dict[param]
    r1 = np.arange(len(envs))
    xdata = []
    for (i, env) in enumerate(envs):
        data = read_hyperparam(alg, env)
        hyperparam_value = data[param]
        xdata.append((hyperparam_range.index(hyperparam_value) + 1))
    barlist = ax.bar(r1, xdata, edgecolor='white')
    for (i, c) in enumerate(['r', 'g', 'b', 'm']):
        barlist[i].set_color(c)
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=30)
    ax.yaxis.set_tick_params(pad=0)
    ax.set_xticklabels([])
    ax.set_yticks(range((len(hyperparam_range) + 1)))
    if ('learning_rate' in param):
        hyperparam_range = ['3e-5', '3e-4']
    ax.set_yticklabels(['', *hyperparam_range])
    ax.margins(x=0.0, y=0.0, tight=True)
    return barlist

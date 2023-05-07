from matplotlib import pyplot as plt
import numpy as np
import torch
import os
import yaml
import math
import argparse


def plot_hyperparam_alg(ax, alg):
    relevant_dict = relevant_param(alg)
    ylabel = list(relevant_dict.keys())
    xdata = []
    r1 = np.arange(len(ylabel))
    barWidth = 0.2
    color = ['r', 'g', 'b', 'm']
    for (i, env) in enumerate(envs):
        data = read_hyperparam(alg, env)
        xdata = []
        for key in ylabel:
            hyperparam_range = relevant_dict[key]
            hyperparam_value = data[key]
            xdata.append((hyperparam_range.index(hyperparam_value) + 1))
        r = [(x + (i * barWidth)) for x in r1]
        ax.bar(r, xdata, color=color[i], width=barWidth, edgecolor='white', label=env)
    ax.set_xticks([(r + barWidth) for r in range(len(ylabel))])
    ax.set_xticklabels(ylabel)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30)
    ax.set_ylabel(alg)
    ax.set_yticklabels([])

from matplotlib import pyplot as plt
import numpy as np
import torch
import os
import yaml
import math
import argparse


def plot_hyperparam_env(ax, env):
    ylabel = list(relevant_param('AIRL').keys())
    r1 = np.arange(len(ylabel))
    barWidth = 0.125
    for (i, alg) in enumerate(algorithms):
        relevant_dict = relevant_param(alg)
        data = read_hyperparam(alg, env)
        xdata = []
        for key in ylabel:
            if (key in relevant_dict.keys()):
                hyperparam_range = relevant_dict[key]
                hyperparam_value = data[key]
                xdata.append((hyperparam_range.index(hyperparam_value) + 1))
            else:
                xdata.append(0)
        r = [(x + (i * barWidth)) for x in r1]
        ax.bar(r, xdata, color=colors[i], width=barWidth, edgecolor='white', label=alg)
    ax.set_xticks([(r + barWidth) for r in range(len(ylabel))])
    ax.set_ylabel(env)
    ax.set_yticklabels([])
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30)

from matplotlib import pyplot as plt
import numpy as np
import torch
import os
import yaml
import math
import argparse


def plot_environment_result(data, ax, env):
    ax.set_title(ENV_NAMES[env], fontsize=fontsize)
    pre_print = ('For env: ' + env)
    print(pre_print)
    plot_env_baseline(ax, env)
    for (alg, col) in zip(algorithms, colors):
        try:
            metric = data[alg]
            (x, mean, std_err, std) = process_test_data(metric)
            if (alg == 'BC'):
                x = np.multiply(x, np.linspace(0.0, 100.0, num=100))
                mean = np.repeat(mean, 100)
                std_err = np.repeat(std_err, 100)
                std = np.repeat(std, 100)
            x_pow = math.floor(math.log(x[(- 1)], 10))
            x = (x / (10 ** x_pow))
            ax.plot(x, mean, col, label=alg)
            ax.fill_between(x, (mean - std_err), (mean + std_err), color=col, alpha=0.3)
            result = ((((((' ' * len(pre_print)) + alg) + ', Result: ') + '{:.2f}'.format(mean[(- 1)])) + ' +/- ') + '{:.2f}'.format(std[(- 1)]))
            print(result)
        except Exception as e:
            print(((('\t no ' + alg) + ' data for env:') + env))
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=40)
    ax.margins(x=0.0, tight=True)

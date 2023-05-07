from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_comparison(extension):
    yolo_air_path = os.path.join(data_dir, 'comparison/run_search_yolo-air-run_env=size=14-in-colour=False-task=arithmetic-ops=addition_alg=yolo-air_duration=long_seed=0_2018_07_16_13_46_48/')
    air_path = os.path.join(data_dir, 'comparison/run_search_air-run_env=size=14-in-colour=False-task=arithmetic-ops=addition_alg=attend-infer-repeat_duration=long_seed=0_2018_07_24_13_02_34')
    dair_path = os.path.join(data_dir, 'comparison/run_search_dair-run_env=size=14-in-colour=False-task=arithmetic-ops=addition_alg=attend-infer-repeat_duration=long_seed=0_2018_07_10_09_22_24')
    baseline_path = os.path.join(data_dir, 'comparison/run_search_comparison-baseline_env=size=14-in-colour=False-task=arithmetic-ops=addition_alg=baseline_duration=oak_seed=0_2018_07_20_11_15_24/')
    fig = plt.figure(figsize=(5, 3.5))
    ax = plt.gca()
    y_func = (lambda y: (100 * y))
    (x, y, *yerr) = get_arithmetic_data([yolo_air_path], 'n_digits', '_test_AP', 0, 'ci95', y_func=y_func)
    line = ax.errorbar(x, y, yerr=yerr, label='SPAIR', marker='o', ls='-')
    line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([air_path], 'n_digits', '_test_AP', 0, 'ci95', y_func=y_func)
    line = ax.errorbar(x, y, yerr=yerr, label='AIR', marker='^', ls='-.')
    line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([dair_path], 'n_digits', 'AP', 0, 'ci95', y_func=y_func)
    line = ax.errorbar(x, y, yerr=yerr, label='DAIR', marker='v', ls='--')
    line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([baseline_path], 'n_digits', '_test_AP', 0, 'ci95', y_func=y_func)
    ax.plot(x, y, label='ConnComp', marker='s', ls=':')
    ax.set_ylabel('Average Precision', fontsize=12)
    ax.set_xlabel('\\# Digits in Image', fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_ylim((0.0, 105.0))
    ax.set_xticks(x)
    plt.legend(loc='upper right', handlelength=4)
    plt.subplots_adjust(left=0.12, bottom=0.13, right=0.99, top=0.99)
    plot_path = os.path.join(plot_dir, ('comparison/main.' + extension))
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    fig.savefig(plot_path)
    plt.show()

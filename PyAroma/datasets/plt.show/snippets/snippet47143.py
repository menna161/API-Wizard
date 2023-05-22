from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_ablation(extension):
    yolo_path_n_lookback_0 = os.path.join(data_dir, 'ablation/run_search_yolo-air-ablation-n-lookback=0_env=task=scatter_alg=yolo-air-transfer_duration=long_seed=0_2018_09_03_08_52_37/')
    yolo_path_n_lookback_1 = os.path.join(data_dir, 'ablation/run_search_yolo-air-ablation-n-lookback=1_env=task=scatter_alg=yolo-air-transfer_duration=long_seed=0_2018_09_03_09_00_25/')
    (fig, axes) = plt.subplots(1, 3, figsize=(8, 2.2))
    ax = axes[0]
    y_func = (lambda y: (100 * y))
    measure = '_test_AP'
    key_filter = (lambda key: (key.min_chars not in [1, 6]))
    nb0_data = get_transfer_data(yolo_path_n_lookback_0, 'n_train', measure, 'ci95', y_func=y_func)
    for ((x, y, *yerr), key) in nb0_data:
        if (not key_filter(key)):
            continue
        label = 'No Lateral Conns, {}--{} digits'.format(key.min_chars, key.max_chars)
        ax.errorbar(x, y, yerr=yerr, label=label)
    nb1_data = get_transfer_data(yolo_path_n_lookback_1, 'n_train', measure, 'ci95', y_func=y_func)
    for ((x, y, *yerr), key) in nb1_data:
        if (not key_filter(key)):
            continue
        label = 'With Lateral Conns, {}--{} digits'.format(key.min_chars, key.max_chars)
        ax.errorbar(x, y, yerr=yerr, label=label)
    fontsize = None
    labelsize = None
    ax.set_ylabel('Average Precision', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.set_ylim((0.0, 105.0))
    ax.set_xlabel('\\# Digits in Test Image', fontsize=fontsize)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.legend(loc='lower left', fontsize=8)
    ax = axes[1]
    measure = '_test_count_1norm'
    nb0_data = get_transfer_data(yolo_path_n_lookback_0, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in nb0_data:
        if (not key_filter(key)):
            continue
        ax.errorbar(x, y, yerr=yerr)
    nb1_data = get_transfer_data(yolo_path_n_lookback_1, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in nb1_data:
        if (not key_filter(key)):
            continue
        ax.errorbar(x, y, yerr=yerr)
    ax.set_ylabel('Count Absolute Error', fontsize=fontsize)
    ax.set_xlabel('\\# Digits in Test Image', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.set_ylim((0.0, 4.0))
    ax.set_xticks([0, 5, 10, 15, 20])
    ax = axes[2]
    measure = '_test_count_error'
    nb0_data = get_transfer_data(yolo_path_n_lookback_0, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in nb0_data:
        if (not key_filter(key)):
            continue
        ax.errorbar(x, y, yerr=yerr)
    nb1_data = get_transfer_data(yolo_path_n_lookback_1, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in nb1_data:
        if (not key_filter(key)):
            continue
        ax.errorbar(x, y, yerr=yerr)
    ax.set_ylabel('Count 0-1 Error', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.set_ylim((0.0, 1.05))
    ax.set_xlabel('\\# Digits in Test Image', fontsize=fontsize)
    ax.set_xticks([0, 5, 10, 15, 20])
    plt.subplots_adjust(left=0.07, bottom=0.2, right=0.98, top=0.94, wspace=0.27)
    plot_path = os.path.join(plot_dir, ('ablation/main.' + extension))
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    fig.savefig(plot_path)
    plt.show()

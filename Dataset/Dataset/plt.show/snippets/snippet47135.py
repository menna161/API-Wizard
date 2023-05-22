from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_transfer(extension):
    yolo_path = os.path.join(data_dir, 'transfer/run_search_yolo-air-transfer_env=size=14-in-colour=False-task=scatter_alg=yolo-air-transfer_duration=long_seed=0_2018_07_19_14_21_39/')
    baseline_path_ap = os.path.join(data_dir, 'transfer/run_search_transfer-baseline_env=size=14-in-colour=False-task=scatter_alg=baseline_duration=oak_seed=0_2018_07_20_11_27_19/')
    baseline_path_count_1norm = os.path.join(data_dir, 'transfer/run_search_transfer-baseline-sc=count-1norm_env=size=14-in-colour=False-task=scatter_alg=baseline_duration=oak_seed=0_2018_07_26_12_15_50/')
    baseline_path_count_error = os.path.join(data_dir, 'transfer/run_search_transfer-baseline-sc=count-error_env=size=14-in-colour=False-task=scatter_alg=baseline_duration=oak_seed=0_2018_07_26_12_29_21/')
    (fig, axes) = plt.subplots(1, 3, figsize=(8, 2.2))
    ax = axes[0]
    y_func = (lambda y: (100 * y))
    measure = '_test_AP'
    yolo_data = get_transfer_data(yolo_path, 'n_train', measure, 'ci95', y_func=y_func)
    for ((x, y, *yerr), key) in yolo_data:
        label = 'Trained on {}--{} digits'.format(key.min_chars, key.max_chars)
        ax.errorbar(x, y, yerr=yerr, label=label)
    (x, y) = get_transfer_baseline_data(baseline_path_ap, 'n_train', measure, 'ci95', y_func=y_func)
    ax.plot(x, y, label='ConnComp')
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
    yolo_data = get_transfer_data(yolo_path, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in yolo_data:
        label = 'Trained on {}--{} digits'.format(key.min_chars, key.max_chars)
        ax.errorbar(x, y, yerr=yerr, label=label)
    (x, y) = get_transfer_baseline_data(baseline_path_count_1norm, 'n_train', measure, 'ci95')
    ax.plot(x, y, label='ConnComp')
    ax.set_ylabel('Count Absolute Error', fontsize=fontsize)
    ax.set_xlabel('\\# Digits in Test Image', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.set_ylim((0.0, 3.1))
    ax.set_xticks([0, 5, 10, 15, 20])
    ax = axes[2]
    measure = '_test_count_error'
    yolo_data = get_transfer_data(yolo_path, 'n_train', measure, 'ci95')
    for ((x, y, *yerr), key) in yolo_data:
        label = 'Trained on {}--{} digits'.format(key.min_chars, key.max_chars)
        ax.errorbar(x, y, yerr=yerr, label=label)
    (x, y) = get_transfer_baseline_data(baseline_path_count_error, 'n_train', measure, 'ci95')
    ax.plot(x, y, label='ConnComp')
    ax.set_ylabel('Count 0-1 Error', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.set_ylim((0.0, 1.05))
    ax.set_xlabel('\\# Digits in Test Image', fontsize=fontsize)
    ax.set_xticks([0, 5, 10, 15, 20])
    plt.subplots_adjust(left=0.07, bottom=0.2, right=0.98, top=0.94, wspace=0.27)
    plot_path = os.path.join(plot_dir, ('transfer/main.' + extension))
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    fig.savefig(plot_path)
    plt.show()

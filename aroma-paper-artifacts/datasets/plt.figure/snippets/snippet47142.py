from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_addition(extension):
    air_fixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=fixed_alg=air-math_duration=long_seed=0_2018_07_29_09_58_58/')
    baseline_fixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=fixed_alg=baseline-math_duration=long_seed=0_2018_07_28_22_01_21/')
    ground_truth_fixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=fixed_alg=ground-truth-math_duration=long_seed=0_2018_07_28_22_02_14/')
    simple_fixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=fixed_alg=simple-math_duration=long_seed=0_2018_07_28_22_03_18/')
    yolo_air_fixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=fixed_alg=yolo-air-math_duration=long_seed=0_2018_07_28_22_04_04/')
    baseline_raw_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=raw_alg=baseline-math_duration=long_seed=0_2018_07_28_22_00_58/')
    ground_truth_raw_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=raw_alg=ground-truth-math_duration=long_seed=0_2018_07_28_22_01_56/')
    simple_raw_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=raw_alg=simple-math_duration=long_seed=0_2018_07_28_22_02_59/')
    air_unfixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=unfixed_alg=air-math_duration=long_seed=0_2018_07_29_09_58_32/')
    baseline_unfixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=unfixed_alg=baseline-math_duration=long_seed=0_2018_07_28_22_01_39/')
    ground_truth_unfixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=unfixed_alg=ground-truth-math_duration=long_seed=0_2018_07_28_22_02_30/')
    simple_unfixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=unfixed_alg=simple-math_duration=long_seed=0_2018_07_28_22_03_41/')
    yolo_air_unfixed_path = os.path.join(data_dir, 'addition/stage2/run_search_addition-stage2_env=task=arithmetic2_run-kind=unfixed_alg=yolo-air-math_duration=long_seed=0_2018_07_28_22_04_21/')
    fig = plt.figure(figsize=(5, 4.5))
    ax = plt.gca()
    (x, y, *yerr) = get_arithmetic_data([baseline_raw_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='ConnComp', marker='o', ls='-')
    (x, y, *yerr) = get_arithmetic_data([ground_truth_raw_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='TrueBB', marker='^', ls='-')
    (x, y, *yerr) = get_arithmetic_data([simple_raw_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='ConvNet', marker='v', ls='-')
    (x, y, *yerr) = get_arithmetic_data([yolo_air_fixed_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='SPAIR - Fixed', marker='v', ls='-')
    yolo_air_color = line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([yolo_air_unfixed_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='SPAIR - Unfixed', marker='v', ls='--', color=yolo_air_color)
    (x, y, *yerr) = get_arithmetic_data([air_fixed_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='AIR - Fixed', marker='o', ls='-')
    air_color = line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([air_unfixed_path], 'n_train', '_test_math_accuracy', 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='AIR - Unfixed', marker='o', ls='--', color=air_color)
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('\\# Training Examples / 1000')
    ax.tick_params(axis='both')
    ax.set_ylim((0.0, 1.05))
    ax.set_xscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels((np.array(x) / 1000).astype('i'))
    plt.legend(loc='lower center', handlelength=2.5, bbox_to_anchor=(0.5, 1.01), ncol=3, columnspacing=1)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.82)
    plot_path = os.path.join(plot_dir, ('addition/main.' + extension))
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    fig.savefig(plot_path)
    plt.show()

from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_addition_old(extension):
    yolo_path = os.path.join(data_dir, 'addition/2stage/run_search_sample_complexity_experiment_yolo_air_VS_nips_2018_addition_14x14_kind=long_cedar_seed=0_2018_05_14_03_04_29')
    yolo_supplement_path = os.path.join(data_dir, 'addition/2stage/run_search_supplement_sample_complexity_experiment_yolo_air_VS_nips_2018_addition_14x14_kind=supplement_seed=0_2018_05_14_14_18_26')
    simple_path = os.path.join(data_dir, 'addition/simple/run_search_sample_complexity-size=14_colour=False_task=addition_alg=yolo_math_simple_duration=long_seed=0_2018_05_14_23_59_50')
    simple_2stage_path = os.path.join(data_dir, 'addition/simple_2stage/run_search_sample_complexity-size=14_colour=False_task=addition_alg=yolo_math_simple_2stage_duration=long_seed=0_2018_05_15_12_55_38')
    fig = plt.figure(figsize=(5, 3.5))
    ax = plt.gca()
    measure = 'math_accuracy'
    (x, y, *yerr) = get_arithmetic_data([yolo_path, yolo_supplement_path], 'n_train', measure, 1, 'ci95')
    label = 'SI-AIR'
    ax.errorbar(x, y, yerr=yerr, label=label)
    (x, y, *yerr) = get_arithmetic_data([simple_path], 'n_train', measure, 0, 'ci95')
    label = 'Conv'
    ax.errorbar(x, y, yerr=yerr, label=label)
    (x, y, *yerr) = get_arithmetic_data([simple_2stage_path], 'n_train', measure, 0, 'ci95')
    label = 'Conv - 2stage'
    ax.errorbar(x, y, yerr=yerr, label=label)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_xlabel('\\# Training Samples / 1000', fontsize=12)
    ax.set_title('Addition - Between 1 and 11 numbers', fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_ylim((0.0, 1.05))
    ax.set_xticks(x)
    ax.set_xticklabels((np.array(x) / 1000).astype('i'))
    plt.legend(loc='upper left')
    plot_path = os.path.join(plot_dir, ('addition/main.' + extension))
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.subplots_adjust(left=0.12, bottom=0.14, right=0.98, top=0.91)
    fig.savefig(plot_path)
    plt.show()

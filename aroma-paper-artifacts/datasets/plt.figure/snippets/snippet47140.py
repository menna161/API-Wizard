from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_xo_2stage_decoder_kind(extension):
    attn_yolo_path = os.path.join(data_dir, 'xo/pretrained/yolo/run_search_yolo-xo-continue_env=xo_decoder-kind=attn_alg=yolo-xo-continue_duration=long_seed=0_2018_06_07_12_12_19')
    mlp_yolo_path = os.path.join(data_dir, 'xo/pretrained/yolo/run_search_yolo-xo-continue_env=xo_decoder-kind=mlp_alg=yolo-xo-continue_duration=long_seed=0_2018_06_07_12_17_35')
    seq_yolo_path = os.path.join(data_dir, 'xo/pretrained/yolo/run_search_yolo-xo-continue_env=xo_decoder-kind=seq_alg=yolo-xo-continue_duration=long_seed=0_2018_06_07_12_13_03')
    attn_simple_path = os.path.join(data_dir, 'xo/full/simple/run_search_conv-xo_env=xo_decoder-kind=attn_alg=simple-xo_duration=long_seed=0_2018_06_08_17_49_36')
    mlp_simple_path = os.path.join(data_dir, 'xo/full/simple/run_search_conv-xo_env=xo_decoder-kind=mlp_alg=simple-xo_duration=long_seed=0_2018_06_08_17_50_40')
    seq_simple_path = os.path.join(data_dir, 'xo/full/simple/run_search_conv-xo_env=xo_decoder-kind=seq_alg=simple-xo_duration=long_seed=0_2018_06_08_17_50_20')
    plt.figure(figsize=(5, 3.5))
    ax = plt.gca()
    measure = 'math_accuracy'
    (x, y, *yerr) = get_arithmetic_data([attn_yolo_path], 'n_train', measure, 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='attn-yolo')
    attn_colour = line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([mlp_yolo_path], 'n_train', measure, 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='mlp-yolo')
    mlp_colour = line.lines[0].get_c()
    (x, y, *yerr) = get_arithmetic_data([seq_yolo_path], 'n_train', measure, 0, 'ci95')
    line = ax.errorbar(x, y, yerr=yerr, label='seq-yolo')
    seq_colour = line.lines[0].get_c()
    measure = 'math_accuracy'
    (x, y, *yerr) = get_arithmetic_data([attn_simple_path], 'n_train', measure, 0, 'ci95')
    ax.errorbar(x, y, yerr=yerr, label='attn-simple', c=attn_colour, ls='--')
    (x, y, *yerr) = get_arithmetic_data([mlp_simple_path], 'n_train', measure, 0, 'ci95')
    ax.errorbar(x, y, yerr=yerr, label='mlp-simple', c=mlp_colour, ls='--')
    (x, y, *yerr) = get_arithmetic_data([seq_simple_path], 'n_train', measure, 0, 'ci95')
    ax.errorbar(x, y, yerr=yerr, label='seq-simple', c=seq_colour, ls='--')
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_xlabel('\\# Training Samples', fontsize=12)
    ax.tick_params(axis='both', labelsize=14)
    ax.set_ylim((0.0, 1.05))
    ax.set_xticks(x)
    plt.legend()
    plt.show()

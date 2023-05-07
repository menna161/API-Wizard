from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def plot_core_sample_complexity():
    path = 'core/run_search_sample_complexity-size=14_colour=False_task=arithmetic_alg=yolo_math_simple_2stage_duration=long_seed=0_2018_05_15_12_59_19'
    path = os.path.join(data_dir, path)
    ax = plt.gca()
    (x, y, *yerr) = get_stage_data(path, 0, 'n_train', 'stopping_criteria', 'ci95', (lambda error: (1 - error)))
    label = 'test'
    ax.errorbar(x, y, yerr=yerr, label=label, ls='--')
    plt.show()

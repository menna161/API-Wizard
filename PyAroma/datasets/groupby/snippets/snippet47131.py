from cycler import cycler
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dps.hyper import HyperSearch
from dps.utils import process_path, Config, sha_cache, set_clear_cache, confidence_interval, standard_error
from matplotlib import rc


def get_stage_data(path, stage_idx, x_key, y_key, spread_measure, y_func=None):
    y_func = (y_func or (lambda x: x))
    df = _get_stage_data_helper(path, stage_idx)
    groups = sorted(df.groupby(x_key))
    x = [v for (v, _df) in groups]
    ys = [y_func(_df[y_key]) for (v, _df) in groups]
    y = [_y.mean() for _y in ys]
    (y_upper, y_lower) = spread_measures[spread_measure](ys)
    return np.stack([x, y, y_upper, y_lower])

import os
import numpy as np
import pandas as pd
from whynot.framework import GenericExperiment, parameter


def load_dataset():
    'Load the LaLonde dataset.'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(dir_path, 'lalonde.csv')
    lalonde = pd.read_csv(data_path, index_col=0)
    lalonde = lalonde.drop('re78', axis=1)
    return lalonde.rename(columns={'treat': 'treatment'})

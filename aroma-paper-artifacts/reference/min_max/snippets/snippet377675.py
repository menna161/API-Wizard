import itertools
from operator import itemgetter
import os
from colour import Color, color_scale, hsl2hex
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.lines import Line2D
from scipy.stats import zscore
from sklearn.preprocessing import MinMaxScaler
from .benchmark import generate_tests


def standardize_scale(runs_df, target, invert=False):
    runs_df = runs_df.copy()
    print('Standardizing and scaling {}...'.format(target))
    m_type = ('classification' if (target == 'F1_SCORE') else 'regression')
    d_ids = pd.unique(runs_df[(runs_df['TYPE'] == m_type)]['DATASET_ID'].values)
    for d_id in d_ids:
        transformation = MinMaxScaler().fit_transform(zscore(runs_df[(runs_df['DATASET_ID'] == d_id)][target].values).reshape(((- 1), 1))).ravel()
        runs_df.loc[((runs_df['DATASET_ID'] == d_id), target)] = ((1 - transformation) if invert else transformation)
    return runs_df

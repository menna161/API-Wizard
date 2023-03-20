import os
import numpy as np
from itertools import product
from atol.utils import compute_tda_for_graphs
from atol.utils import graph_dtypes, csv_toarray, atol_feats_graphs
from atol import Atol
from sklearn.cluster import MiniBatchKMeans
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from atol.utils import graph_tenfold


def renormalize(df):
    df['value'] = MinMaxScaler().fit_transform(df['value'].values.reshape((- 1), 1))
    return df

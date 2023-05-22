import re
from math import atan2
import numpy as np
import pandas as pd
import paper_reviewer_matcher as pp
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, create_assignment
from scipy.cluster.hierarchy import linkage
from sklearn.preprocessing import MinMaxScaler
from itertools import product
from tqdm import tqdm, tqdm_notebook
from sklearn.manifold import MDS
from copkmeans.cop_kmeans import cop_kmeans


def calculate_timezone_distance_matrix(df):
    '\n    Calculate timezone distance matrix from a given dataframe\n    '
    n_users = len(df)
    timezone_df = df[['idx', 'timezone', 'second_timezone']]
    timezone_df.loc[(:, 'timezone')] = timezone_df.timezone.map((lambda t: remove_text_parentheses(t).split(' ')[(- 1)]))
    timezone_df.loc[(:, 'second_timezone')] = timezone_df.second_timezone.map((lambda t: remove_text_parentheses(t).split(' ')[(- 1)].replace('me', ' ')))
    timezone_list = timezone_df.to_dict(orient='records')
    D_tz = np.zeros((n_users, n_users))
    for (d1, d2) in product(timezone_list, timezone_list):
        (idx1, idx2, tz_dist) = compute_tz_distance_dict(d1, d2)
        D_tz[(idx1, idx2)] = tz_dist
    return D_tz

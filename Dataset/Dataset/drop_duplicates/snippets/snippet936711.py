from torch.utils.data import Dataset
import pickle as pkl
import torch
import pandas as pd
from pandas import DataFrame as df


def __init__(self, pkl_file, drop_dup=False):
    df = pkl.load(open(pkl_file, 'rb'))
    if (drop_dup == True):
        df_user = df.drop_duplicates(['user_id'])
        df_movie = df.drop_duplicates(['movie_id'])
        self.dataFrame = pd.concat((df_user, df_movie), axis=0)
    else:
        self.dataFrame = df

import argparse
from glob import glob
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from data_gen import CHAR_IDX
from utils import LogicSeq
from models import build_model
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from mpl_toolkits.mplot3d import Axes3D


def plot_len():
    'Plot increasing length results.'
    df = pd.read_csv('len_results.csv')
    df['Mean'] = df.iloc[(:, 5:)].mean(axis=1)
    idx = df.groupby(['Model', 'Dim', 'Symbol'])['Mean'].idxmax()
    df = df.loc[idx]
    df = df.drop(columns=['Mean'])
    df = pd.melt(df, id_vars=['Training', 'Model', 'Dim', 'Symbol', 'Run'], var_name='Len', value_name='Acc')
    df['Len'] = df['Len'].astype(int)
    df = df[((df['Dim'] == ARGS.dim) & (~ df['Model'].isin(['imasm', 'imarsm'])))]
    print(df.head())
    sns.set_style('whitegrid')
    sns.lineplot(x='Len', y='Acc', hue='Model', style='Symbol', data=df, sort=True)
    plt.ylim(0.4, 1.0)
    plt.ylabel('Accuracy')
    plt.xlim(2, 64)
    plt.xlabel('Length of symbols')
    showsave_plot()

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


def plot_nstep():
    'Plot nstep results.'
    df = pd.read_csv('nstep_results.csv')
    df['Mean'] = df.iloc[(:, 4:)].mean(axis=1)
    idx = df.groupby(['Model', 'Dim'])['Mean'].idxmax()
    df = df.loc[idx]
    df = df.drop(columns=['Mean'])
    df = pd.melt(df, id_vars=['Training', 'Model', 'Dim', 'Run'], var_name='NStep', value_name='Acc')
    df['NStep'] = df['NStep'].astype(int)
    df = df[(df['Dim'] == ARGS.dim)]
    print(df.head())
    sns.set_style('whitegrid')
    sns.lineplot(x='NStep', y='Acc', hue='Model', data=df, sort=True)
    plt.vlines(3, 0.4, 1.0, colors='grey', linestyles='dashed', label='training')
    plt.ylim(0.4, 1.0)
    plt.ylabel('Accuracy')
    plt.xlim(1, 32)
    plt.xlabel('# of steps')
    showsave_plot()

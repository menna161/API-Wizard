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


def plot_dim():
    'Plot increasing dimension over increasing difficulty.'
    df = pd.read_csv('results.csv')
    df = df[((df['Model'] == ARGS.model) & (df['Training'] == 'curr'))]
    print(df.head())
    sns.set_style('whitegrid')
    sns.lineplot(x='Dim', y='Mean', hue='Set', data=df, hue_order=['validation', 'easy', 'medium', 'hard'])
    plt.ylim(0.5, 1.0)
    plt.ylabel('Mean Accuracy')
    plt.xlim(32, 128)
    plt.xlabel('Dimension')
    plt.legend(loc='upper left')
    showsave_plot()

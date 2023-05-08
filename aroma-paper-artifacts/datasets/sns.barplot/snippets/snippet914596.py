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


def plot_training():
    'Plot training method on mean accuracy per test set.'
    df = pd.read_csv('results.csv')
    df = df[(df['Model'] == ARGS.model)]
    print(df.head())
    sns.set_style('whitegrid')
    sns.barplot(x='Training', y='Mean', hue='Set', errwidth=1.2, capsize=0.025, data=df)
    plt.ylabel('Mean Accuracy')
    plt.ylim(0.5, 1.0)
    showsave_plot()

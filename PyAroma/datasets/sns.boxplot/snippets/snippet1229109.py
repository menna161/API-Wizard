import sys
from time import time
from scipy import stats, sparse
from scipy.sparse.linalg import svds, eigs
from scipy.special import expit
import numpy as np
import os
import math
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE
from sklearn.metrics import precision_recall_curve
from sklearn import metrics
import collections
from scipy.stats import norm as dist_model
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.cross_decomposition import CCA
import pandas as pd
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
from collections import defaultdict
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
import matplotlib as mpl
import matplotlib.colors as pltcolors


def plot_auc_region_violin(datas, jitter_datas, fig_file, xticks, cutoff, ylabel):
    plt.clf()
    (fig, ax) = plt.subplots(figsize=((FIG_WIDTH * 1.5), FIG_HEIGHT))
    ax = sns.boxplot(data=datas, color='.8')
    ax = sns.stripplot(data=jitter_datas, jitter=True, size=1)
    ax.set_ylabel(ylabel)
    ax.set_xlabel((('Number of seen cell types in the ' + str(cutoff)) + '-hop region'))
    ax.set_xticklabels(xticks)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.savefig(fig_file)

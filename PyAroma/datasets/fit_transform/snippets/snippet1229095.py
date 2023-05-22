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


def plot_umap(embedding, lab, lab2col, file, lab2marker=None, legend=True, size=1, title='', legendmarker=20):
    MEDIUM_SIZE = (8 * 4)
    SMALLER_SIZE = (6 * 4)
    plt.rc('font', size=MEDIUM_SIZE)
    plt.rc('axes', labelsize=MEDIUM_SIZE)
    plt.rc('axes', titlesize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=SMALLER_SIZE)
    plt.rc('ytick', labelsize=SMALLER_SIZE)
    plt.rc('figure', titlesize=MEDIUM_SIZE)
    if (np.shape(embedding)[1] != 2):
        embedding = umap.UMAP(random_state=1).fit_transform(embedding)
    assert (np.shape(embedding)[1] == 2)
    print(size)
    plt.clf()
    (fig, ax) = plt.subplots(figsize=((FIG_WIDTH * 4), (FIG_HEIGHT * 4)))
    for l in lab2col:
        ind = np.where((lab == l))[0]
        if (len(ind) == 0):
            continue
        if (lab2marker is None):
            plt.scatter(embedding[(ind, 0)], embedding[(ind, 1)], c=lab2col[l], label=l, s=size)
        else:
            plt.scatter(embedding[(ind, 0)], embedding[(ind, 1)], c=lab2col[l], label=l, s=size, marker=lab2marker[l])
    if legend:
        plt.legend(loc='lower left', ncol=6, fontsize=6)
    plt.title(title)
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    plt.xlabel('UMAP 1')
    plt.ylabel('UMAP 2')
    plt.tight_layout()
    plt.savefig(file, dpi=100)
    if legend:
        return
    (handles, labels) = ax.get_legend_handles_labels()
    fig_legend = plt.figure(figsize=(6, 6))
    axi = fig_legend.add_subplot(111)
    fig_legend.legend(handles, labels, loc='center', scatterpoints=1, ncol=1, frameon=False, markerscale=legendmarker)
    axi.xaxis.set_visible(False)
    axi.yaxis.set_visible(False)
    plt.savefig((file + '_legend.pdf'), dpi=100)
    plt.gcf().clear()

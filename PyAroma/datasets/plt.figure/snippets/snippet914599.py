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


def plot_single_preds():
    'Plot embeddings of single character predicates.'
    model = create_model(pca=True)
    syms = 'abcdefghijklmnopqrstuvwxyz'
    (ctx, splits) = (list(), list())
    preds = list('pqrv')
    preds.extend([''.join(([e] * 2)) for e in preds])
    for p in preds:
        for c in syms:
            ctx.append('{}({}).'.format(p, c))
        splits.append(len(ctx))
    embds = get_pca(ctx, model, dims=len(preds))
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    prev_sp = 0
    for sp in splits:
        (x, y, z) = (embds[(prev_sp:sp, 0)], embds[(prev_sp:sp, 1)], embds[(prev_sp:sp, (- 1))])
        ax.scatter(x, y, z, depthshade=False)
        for i in map(syms.index, 'fdgm'):
            ax.text(x[i], y[i], z[i], ctx[(prev_sp + i)])
        prev_sp = sp
    showsave_plot()

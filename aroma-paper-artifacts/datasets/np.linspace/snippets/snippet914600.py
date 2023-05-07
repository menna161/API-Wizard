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


def plot_pred_saturation():
    'Plot predicate embedding saturation.'
    model = create_model(pca=True)
    (ctx, splits) = (list(), list())
    for i in range(2, 65):
        p = ''.join((['p'] * i))
        ctx.append('{}(a).'.format(p))
        splits.append(len(ctx))
    embds = get_pca(ctx, model)
    plt.scatter(embds[(::2, 0)], embds[(::2, 1)])
    plt.scatter(embds[(1::2, 0)], embds[(1::2, 1)])
    prev_sp = 0
    for (i, sp) in enumerate(splits):
        (pred, x, y) = (ctx[prev_sp], embds[(prev_sp, 0)], embds[(prev_sp, 1)])
        count = pred.count('p')
        if (count <= 6):
            (xf, yf) = (offset(x), offset(y))
            plt.annotate(pred, xy=(x, y), xytext=(xf, yf), textcoords='offset points', arrowprops={'arrowstyle': '-'})
        elif ((((i % 3) == 0) and (i < 50)) or (i == (len(splits) - 1)) or (i == (len(splits) - 2))):
            pred = (str(count) + '*p(a)')
            (xf, yf) = (offset(x), offset(y))
            plt.annotate(pred, xy=(x, y), xytext=(xf, yf), textcoords='offset points', arrowprops={'arrowstyle': '-'})
        prev_sp = sp
    plt.xlim((- 2), 2)
    (xmin, xmax) = plt.xlim()
    X = np.linspace(xmin, xmax, 40)
    (ymin, ymax) = plt.ylim()
    Y = np.linspace(ymin, ymax, 40)
    (X, Y) = np.meshgrid(X, Y)
    Z = np.sqrt((((X - embds[((- 1), 0)]) ** 2) + ((Y - embds[((- 1), 1)]) ** 2)))
    plt.contour(X, Y, Z, colors='grey', alpha=0.2, linestyles='dashed')
    Z = np.sqrt((((X - embds[((- 2), 0)]) ** 2) + ((Y - embds[((- 2), 1)]) ** 2)))
    plt.contour(X, Y, Z, colors='grey', alpha=0.2, linestyles='dashed')
    showsave_plot()

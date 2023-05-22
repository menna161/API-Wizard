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


def plot_attention():
    'Plot attention vector over given context.'
    model = create_model(iterations=ARGS.iterations, training=False)
    ctxs = ['p(X):-q(X).q(X):-r(X).r(X):-s(X).s(a).s(c).', 'p(X):-q(X);r(X).r(a).q(a).r(b).q(c).', 'p(X):-q(X).p(X):-r(X).p(c).r(a).q(c).']
    (fig, axes) = plt.subplots(1, 6)
    for (i, ctx) in enumerate(ctxs):
        for (j, t) in enumerate(['p(a).', 'p(b).']):
            rs = ctx.split('.')[:(- 1)]
            dgen = LogicSeq([[([(r + '.') for r in rs], t, 0)]], 1, False, False, pad=ARGS.pad)
            out = model.predict_generator(dgen)
            sims = out[:(- 1)]
            out = np.round(np.asscalar(out[(- 1)]), 2)
            sims = np.stack(sims, axis=0).squeeze()
            sims = sims.T
            ticks = ((['()'] if ARGS.pad else []) + ['$\\phi$'])
            axes[((i * 2) + j)].get_xaxis().set_ticks_position('top')
            sns.heatmap(sims, vmin=0, vmax=1, cmap='Blues', yticklabels=((rs + ticks) if ((j % 2) == 0) else False), xticklabels=range(1, (ARGS.iterations + 1)), linewidths=0.5, square=True, cbar=False, ax=axes[((i * 2) + j)])
            axes[((i * 2) + j)].set_xlabel((('p(a) ' + str(out)) if ((j % 2) == 0) else ('p(b) ' + str(out))))
    plt.tight_layout()
    showsave_plot()

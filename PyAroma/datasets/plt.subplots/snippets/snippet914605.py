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


def plot_dual_attention():
    'Plot dual attention vectors of 2 models over given context.'
    modelbw = build_model('imasm', (ARGS.model_dir + 'curr_imasm64_2.h5'), char_size=(len(CHAR_IDX) + 1), dim=ARGS.dim, iterations=ARGS.iterations, training=False)
    modelfw = build_model('fwimarsm', (ARGS.model_dir + 'curr_fwimarsm64.h5'), char_size=(len(CHAR_IDX) + 1), dim=ARGS.dim, iterations=ARGS.iterations, training=False)
    ctxs = ['p(X):-q(X).q(X):-r(X).r(X):-s(X).s(a).s(b).', 'p(X):-q(X);r(X).r(a).q(a).r(b).q(b).', 'p(X):-q(X).p(X):-r(X).p(b).r(a).q(b).']
    (fig, axes) = plt.subplots(1, 6)
    for (i, ctx) in enumerate(ctxs):
        for (j, m) in enumerate([modelbw, modelfw]):
            rs = ctx.split('.')[:(- 1)]
            dgen = LogicSeq([[([(r + '.') for r in rs], 'p(a).', 0)]], 1, False, False, pad=ARGS.pad)
            out = m.predict_generator(dgen)
            sims = out[:(- 1)]
            out = np.round(np.asscalar(out[(- 1)]), 2)
            sims = np.stack(sims, axis=0).squeeze()
            sims = sims.T
            ticks = ((['()'] if ARGS.pad else []) + ['$\\phi$'])
            axes[((i * 2) + j)].get_xaxis().set_ticks_position('top')
            sns.heatmap(sims, vmin=0, vmax=1, cmap='Blues', yticklabels=((rs + ticks) if ((j % 2) == 0) else False), xticklabels=range(1, 5), linewidths=0.5, square=True, cbar=False, ax=axes[((i * 2) + j)])
            axes[((i * 2) + j)].set_xlabel(('backward' if ((j % 2) == 0) else 'forward'))
    plt.tight_layout()
    showsave_plot()

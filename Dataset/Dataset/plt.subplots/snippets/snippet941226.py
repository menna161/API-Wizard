import logging
import math
import os
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import torch
from gilbert2d import gilbert2d_idx
import time


def plot_orders(generation_idx_list, obs, size=5, plot_rows=4, out_path=None, **kwargs):
    'Plot multiple generation coordinate lists in a single figure. A star on the curve\n    denotes the pixel generated last. obs is a three-tuple of input image dimensions,\n    (input-channels-unused, num_rows, num_cols)'
    num = len(generation_idx_list)
    plot_cols = int(math.ceil((num / 4)))
    (fig, axes) = plt.subplots(plot_rows, plot_cols, figsize=((size * plot_cols), (size * plot_rows)))
    (pr, pc) = (0, 0)
    for generation_idx in generation_idx_list:
        ax = (axes[(pr, pc)] if (len(generation_idx_list) > 1) else axes)
        ax.hlines((np.arange((- 1), obs[1]) + 0.5), xmin=(- 0.5), xmax=(obs[2] - 0.5), alpha=0.5)
        ax.vlines((np.arange((- 1), obs[2]) + 0.5), ymin=(- 0.5), ymax=(obs[1] - 0.5), alpha=0.5)
        (rows, cols) = zip(*generation_idx)
        ax.plot(cols, rows, color='r')
        ax.scatter([cols[(- 1)]], [rows[(- 1)]], marker='*', s=100, c='k')
        ax.axis('equal')
        ax.invert_yaxis()
        pc = ((pc + 1) % plot_cols)
        if (pc == 0):
            pr += 1
    if out_path:
        plt.savefig(out_path, **kwargs)
    else:
        plt.show()

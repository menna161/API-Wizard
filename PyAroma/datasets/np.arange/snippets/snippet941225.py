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


def plot_order(generation_idx, obs, out_path=None):
    'Plot generation coordinate list. A star on the curve\n    denotes the pixel generated last. obs is a three-tuple of input image dimensions,\n    (input-channels-unused, num_rows, num_cols)'
    plt.figure(figsize=(3, 3))
    plt.hlines((np.arange((- 1), obs[1]) + 0.5), xmin=(- 0.5), xmax=(obs[2] - 0.5), alpha=0.5)
    plt.vlines((np.arange((- 1), obs[2]) + 0.5), ymin=(- 0.5), ymax=(obs[1] - 0.5), alpha=0.5)
    (rows, cols) = zip(*generation_idx)
    plt.plot(cols, rows, color='r')
    plt.scatter([cols[(- 1)]], [rows[(- 1)]], marker='*', s=100, c='k')
    plt.xticks(np.arange(obs[1]))
    plt.axis('equal')
    plt.gca().invert_yaxis()
    if out_path:
        plt.savefig(out_path)
    else:
        plt.show()

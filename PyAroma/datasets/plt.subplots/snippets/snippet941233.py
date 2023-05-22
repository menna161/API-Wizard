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


def plot_masks(nrows, ncols, generation_order, masks, k=3, out_path=None):
    import time
    (fig, axes) = plt.subplots(nrows, ncols)
    plt.suptitle(f'Kernel masks')
    for (row_major_index, ((r, c), mask)) in enumerate(zip(generation_order, masks)):
        axes[((row_major_index // ncols), (row_major_index % ncols))].imshow(mask, vmin=0, vmax=1)
    plt.setp(axes, xticks=[], yticks=[])
    if out_path:
        plt.savefig(out_path)
    else:
        plt.show()

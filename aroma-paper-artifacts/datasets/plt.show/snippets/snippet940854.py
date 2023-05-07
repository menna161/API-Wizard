from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import os
import sys
import math
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import scipy.misc as sic
import matplotlib.pyplot as plt
from Utils.Equirec2Cube import Equirec2Cube


def plot_figure(cube, equi, equi_gt):
    plt.figure()
    ax1 = plt.subplot2grid((6, 3), (0, 0))
    ax2 = plt.subplot2grid((6, 3), (0, 1))
    ax3 = plt.subplot2grid((6, 3), (0, 2))
    ax4 = plt.subplot2grid((6, 3), (1, 0))
    ax5 = plt.subplot2grid((6, 3), (1, 1))
    ax6 = plt.subplot2grid((6, 3), (1, 2))
    ax7 = plt.subplot2grid((6, 3), (2, 0), colspan=3, rowspan=2)
    ax8 = plt.subplot2grid((6, 3), (4, 0), colspan=3, rowspan=2)
    ax1.imshow(cube[(0, :, :, :)])
    ax2.imshow(cube[(1, :, :, :)])
    ax3.imshow(cube[(2, :, :, :)])
    ax4.imshow(cube[(3, :, :, :)])
    ax5.imshow(cube[(4, :, :, :)])
    ax6.imshow(cube[(5, :, :, :)])
    ax7.imshow(equi)
    ax8.imshow(equi_gt)
    plt.show()

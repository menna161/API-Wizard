from __future__ import print_function
import torch
import numpy as np
from PIL import Image
import random
import inspect, re
import numpy as np
import os
import collections
import math
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from skimage.transform import resize


def make_color_wheel():
    (RY, YG, GC, CB, BM, MR) = (15, 6, 4, 11, 13, 6)
    ncols = (((((RY + YG) + GC) + CB) + BM) + MR)
    colorwheel = np.zeros([ncols, 3])
    col = 0
    colorwheel[(0:RY, 0)] = 255
    colorwheel[(0:RY, 1)] = np.transpose(np.floor(((255 * np.arange(0, RY)) / RY)))
    col += RY
    colorwheel[(col:(col + YG), 0)] = (255 - np.transpose(np.floor(((255 * np.arange(0, YG)) / YG))))
    colorwheel[(col:(col + YG), 1)] = 255
    col += YG
    colorwheel[(col:(col + GC), 1)] = 255
    colorwheel[(col:(col + GC), 2)] = np.transpose(np.floor(((255 * np.arange(0, GC)) / GC)))
    col += GC
    colorwheel[(col:(col + CB), 1)] = (255 - np.transpose(np.floor(((255 * np.arange(0, CB)) / CB))))
    colorwheel[(col:(col + CB), 2)] = 255
    col += CB
    colorwheel[(col:(col + BM), 2)] = 255
    colorwheel[(col:(col + BM), 0)] = np.transpose(np.floor(((255 * np.arange(0, BM)) / BM)))
    col += (+ BM)
    colorwheel[(col:(col + MR), 2)] = (255 - np.transpose(np.floor(((255 * np.arange(0, MR)) / MR))))
    colorwheel[(col:(col + MR), 0)] = 255
    return colorwheel

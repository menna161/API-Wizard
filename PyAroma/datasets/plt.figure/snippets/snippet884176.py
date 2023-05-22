import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
import threading
from matplotlib import collections as mc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import time
import copy
import math
from neural_layout.barnes_hut_tree import *
from matplotlib import pyplot as plt


def __init__(self):
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)
    self.scatter = None
    self.lines = None

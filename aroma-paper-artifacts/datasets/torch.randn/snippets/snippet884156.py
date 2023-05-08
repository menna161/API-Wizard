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


def add_layer(self, name, shape, positions=None, weights=None, colors=None):
    try:
        len(shape)
    except:
        shape = [shape]
    layer_units = np.prod(shape)
    indices = torch.arange(self.num_units, (self.num_units + layer_units), dtype=torch.long)
    indices = indices.view(shape)
    self._num_units += layer_units
    self.layers[name] = indices
    self.layer_connections[name] = []
    if (positions is None):
        positions = torch.randn([layer_units, self.num_dim])
    if (weights is None):
        weights = torch.ones(layer_units)
    if (colors is None):
        colors = torch.ones([layer_units, 4])
    if (self.positions is None):
        self.positions = positions
    else:
        self.positions = torch.cat([self.positions, positions], dim=0)
    if (self.weights is None):
        self.weights = weights
    else:
        self.weights = torch.cat([self.weights, weights], dim=0)
    if (self.colors is None):
        self.colors = colors
    else:
        self.colors = torch.cat([self.colors, colors], dim=0)

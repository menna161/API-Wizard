from __future__ import division
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
import numpy as np


def accuracy(outputs, labels):
    '\n    Compute the accuracy, given the outputs and labels for all images.\n    Returns: (float) accuracy in [0,1]\n    '
    outputs = np.argmax(outputs, axis=1)
    return (np.sum((outputs == labels)) / float(labels.size))

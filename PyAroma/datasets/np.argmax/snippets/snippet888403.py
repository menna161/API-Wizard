import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def accuracy(outputs, labels):
    '\n    Compute the accuracy, given the outputs and labels for all images.\n\n    Returns: (float) accuracy in [0,1]\n    '
    outputs = np.argmax(outputs, axis=1)
    return (np.sum((outputs == labels)) / float(labels.size))

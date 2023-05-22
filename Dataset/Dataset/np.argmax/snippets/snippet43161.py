import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import STNModule
import numpy as np


def accuracy(output, labels):
    corr_output = np.argmax(output, axis=1)
    acc = (np.sum((corr_output == labels)) / float(labels.size))
    return acc

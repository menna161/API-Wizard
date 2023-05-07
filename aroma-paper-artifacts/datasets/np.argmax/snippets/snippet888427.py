import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def accuracy(outputs, labels):
    '\n    Compute the accuracy, given the outputs and labels for all images.\n\n    Args:\n        outputs: (np.ndarray) dimension batch_size x 6 - log softmax output of the model\n        labels: (np.ndarray) dimension batch_size, where each element is a value in [0, 1, 2, 3, 4, 5]\n\n    Returns: (float) accuracy in [0,1]\n    '
    outputs = np.argmax(outputs, axis=1)
    return (np.sum((outputs == labels)) / float(labels.size))

import numpy as np
import torch
import warnings
import torch.nn as nn
import torch.nn.functional as F


def shift(shape, stride, anchors):
    shift_x = ((np.arange(0, shape[1]) + 0.5) * stride)
    shift_y = ((np.arange(0, shape[0]) + 0.5) * stride)
    (shift_x, shift_y) = np.meshgrid(shift_x, shift_y)
    shifts = np.vstack((shift_x.ravel(), shift_y.ravel(), shift_x.ravel(), shift_y.ravel())).transpose()
    A = anchors.shape[0]
    K = shifts.shape[0]
    all_anchors = (anchors.reshape((1, A, 4)) + shifts.reshape((1, K, 4)).transpose((1, 0, 2)))
    all_anchors = all_anchors.reshape(((K * A), 4))
    return all_anchors

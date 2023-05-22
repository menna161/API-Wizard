import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def shift(shape, stride, anchors):
    shift_h = (np.arange(0, shape[0]) * stride)
    shift_w = (np.arange(0, shape[1]) * stride)
    (shift_h, shift_w) = np.meshgrid(shift_h, shift_w)
    shifts = np.vstack((shift_h.ravel(), shift_w.ravel())).transpose()
    A = anchors.shape[0]
    K = shifts.shape[0]
    all_anchors = (anchors.reshape((1, A, 2)) + shifts.reshape((1, K, 2)).transpose((1, 0, 2)))
    all_anchors = all_anchors.reshape(((K * A), 2))
    return all_anchors

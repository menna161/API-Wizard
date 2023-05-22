import os
import numpy as np
from PIL import Image
import torch
from torch import nn
import torch.nn.init as initer


def intersectionAndUnion(output, target, K, ignore_index=255):
    assert (output.ndim in [1, 2, 3])
    assert (output.shape == target.shape)
    output = output.reshape(output.size).copy()
    target = target.reshape(target.size)
    output[np.where((target == ignore_index))[0]] = ignore_index
    intersection = output[np.where((output == target))[0]]
    (area_intersection, _) = np.histogram(intersection, bins=np.arange((K + 1)))
    (area_output, _) = np.histogram(output, bins=np.arange((K + 1)))
    (area_target, _) = np.histogram(target, bins=np.arange((K + 1)))
    area_union = ((area_output + area_target) - area_intersection)
    return (area_intersection, area_union, area_target)

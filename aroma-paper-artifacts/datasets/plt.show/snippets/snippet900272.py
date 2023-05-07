import os
from os.path import join as pjoin
import collections
import json
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.utils import data


def decode_segmap(self, label_mask, plot=False):
    'Decode segmentation class labels into a color image\n        Args:\n            label_mask (np.ndarray): an (M,N) array of integer values denoting\n              the class label at each spatial location.\n            plot (bool, optional): whether to show the resulting color image\n              in a figure.\n        Returns:\n            (np.ndarray, optional): the resulting decoded color image.\n        '
    label_colours = self.get_seismic_labels()
    r = label_mask.copy()
    g = label_mask.copy()
    b = label_mask.copy()
    for ll in range(0, self.n_classes):
        r[(label_mask == ll)] = label_colours[(ll, 0)]
        g[(label_mask == ll)] = label_colours[(ll, 1)]
        b[(label_mask == ll)] = label_colours[(ll, 2)]
    rgb = np.zeros((label_mask.shape[0], label_mask.shape[1], 3))
    rgb[(:, :, 0)] = (r / 255.0)
    rgb[(:, :, 1)] = (g / 255.0)
    rgb[(:, :, 2)] = (b / 255.0)
    if plot:
        plt.imshow(rgb)
        plt.show()
    else:
        return rgb

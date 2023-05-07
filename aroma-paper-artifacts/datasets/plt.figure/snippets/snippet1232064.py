import torch
import torch.nn as nn
import torchvision
import sys
import numpy as np
from PIL import Image
import PIL
import numpy as np
import matplotlib.pyplot as plt


def plot_image_grid(images_np, nrow=8, factor=1, interpolation='lanczos'):
    'Draws images in a grid\n    \n    Args:\n        images_np: list of images, each image is np.array of size 3xHxW of 1xHxW\n        nrow: how many images will be in one row\n        factor: size if the plt.figure \n        interpolation: interpolation used in plt.imshow\n    '
    n_channels = max((x.shape[0] for x in images_np))
    assert ((n_channels == 3) or (n_channels == 1)), 'images should have 1 or 3 channels'
    images_np = [(x if (x.shape[0] == n_channels) else np.concatenate([x, x, x], axis=0)) for x in images_np]
    grid = get_image_grid(images_np, nrow)
    plt.figure(figsize=((len(images_np) + factor), (12 + factor)))
    if (images_np[0].shape[0] == 1):
        plt.imshow(grid[0], cmap='gray', interpolation=interpolation)
    else:
        plt.imshow(grid.transpose(1, 2, 0), interpolation=interpolation)
    plt.show()
    return grid
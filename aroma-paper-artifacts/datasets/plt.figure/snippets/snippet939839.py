import numpy as np
import torch
import torchvision
import torch.nn.functional as F
import matplotlib.pyplot as plt
from PIL import Image


def imshow_rgb(images, nrow, ncol):
    '\n    Parameters\n    ----------\n    images : numpy.ndarray \n             shape [h, w, c]\n    '
    (h, w, c) = images.shape
    fig = plt.figure()
    plt.imshow(images)
    return fig

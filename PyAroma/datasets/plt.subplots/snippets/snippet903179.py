import os
import time
import logging
import operator
import numpy as np
import coloredlogs
from PIL import Image
import Utils
from Utils.shortcuts import channel_last
from matplotlib import pyplot as plt


def plot_image(images, name, shape=None, figsize=(10, 10)):
    images = [np.minimum(np.maximum(img, 0.0), 1.0) for img in images]
    images = channel_last(images, is_array=True)
    len_list = len(images)
    im_list = []
    for i in range(len_list):
        im_list.append(images[i])
    if (shape is None):
        unit = int((len_list ** 0.5))
        shape = (unit, unit)
    imshape = im_list[0].shape
    if (imshape[2] == 1):
        im_list = [np.repeat(im, 3, axis=2) for im in im_list]
    else:
        im_list = [im for im in im_list]
    (fig, axes) = plt.subplots(nrows=shape[1], ncols=shape[1], figsize=figsize)
    for (idx, image) in enumerate(im_list):
        row = (idx // shape[0])
        col = (idx % shape[1])
        axes[(row, col)].axis('off')
        axes[(row, col)].imshow(image, cmap='gray', aspect='auto')
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.tight_layout()
    plt.savefig(name)
    plt.close(fig)

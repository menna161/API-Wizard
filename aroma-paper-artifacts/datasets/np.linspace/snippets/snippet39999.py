import os
import numpy as np
from glob import glob
import tifffile
from keras.applications import imagenet_utils
from keras.utils import to_categorical
from albumentations import PadIfNeeded, HorizontalFlip, VerticalFlip, CenterCrop, Crop, Compose, Transpose, RandomRotate90, ElasticTransform, GridDistortion, OpticalDistortion, RandomSizedCrop, OneOf, CLAHE, RandomContrast, RandomGamma, RandomBrightness


def get_blocks(params):
    '\n    Create blocks using the image dimensions, block size and overlap.\n    :param params: input parameters from params.py\n    :return: List of start row/col indices of the blocks\n    '
    blocks = []
    (yEnd, xEnd) = np.subtract(params.IMG_SZ, params.BLOCK_SZ)
    x = np.linspace(0, xEnd, (np.ceil((xEnd / np.float((params.BLOCK_SZ[1] - params.BLOCK_MIN_OVERLAP)))) + 1), endpoint=True).astype('int')
    y = np.linspace(0, yEnd, (np.ceil((yEnd / np.float((params.BLOCK_SZ[0] - params.BLOCK_MIN_OVERLAP)))) + 1), endpoint=True).astype('int')
    for currx in x:
        for curry in y:
            blocks.append((currx, curry))
    return blocks

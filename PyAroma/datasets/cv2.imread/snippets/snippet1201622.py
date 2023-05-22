import os
import warnings
from skimage import measure
from skimage.morphology import dilation, square, watershed
from multiprocessing.pool import Pool
from os import path
import click
import numpy as np
from scipy.ndimage import binary_erosion
import random
import cv2
from scipy.ndimage import label


def save_mask_and_label(image_name):
    mask_path = os.path.join('train_labels', 'masks', image_name)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    (labeled_array, _) = label(mask)
    label_path = os.path.join('train_labels', 'labels', image_name)
    os.makedirs(os.path.join('train_labels', 'labels'), exist_ok=True)
    cv2.imwrite(label_path, labeled_array)
    create_mask(image_name[:(- 4)], 'train_labels')

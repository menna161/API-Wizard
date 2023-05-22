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


def create_mask(img_id, data_dir):
    labels_dir = os.path.join(data_dir, 'labels')
    masks_dir = os.path.join(data_dir, 'masks_all')
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    labels = cv2.imread(path.join(labels_dir, '{0}.tif'.format(img_id)), cv2.IMREAD_UNCHANGED)
    final_mask = np.zeros((labels.shape[0], labels.shape[1], 3))
    if (np.sum(labels) == 0):
        cv2.imwrite(path.join(masks_dir, '{0}.png'.format(img_id)), final_mask, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        return final_mask
    ships_num = np.max(labels)
    if (ships_num > 0):
        for i in range(1, (ships_num + 1)):
            ship_mask = np.zeros_like(labels, dtype='bool')
            ship_mask[(labels == i)] = 1
            area = np.sum(ship_mask)
            if (area < 200):
                contour_size = 1
            elif (area < 500):
                contour_size = 2
            else:
                contour_size = 3
            eroded = binary_erosion(ship_mask, iterations=contour_size)
            countour_mask = (ship_mask ^ eroded)
            final_mask[(..., 0)] += ship_mask
            final_mask[(..., 1)] += countour_mask
    final_mask[(..., 2)] = create_separation(labels)
    msk = np.clip((final_mask * 255), 0, 255)
    cv2.imwrite(path.join(masks_dir, '{0}.png'.format(img_id)), msk, [cv2.IMWRITE_PNG_COMPRESSION, 9])

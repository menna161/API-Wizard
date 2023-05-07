import random
import numpy as np
import scipy
from scipy import ndimage
from PIL import Image, ImageEnhance, ImageOps


def rotate(img, magnitude):
    img = np.array(img)
    magnitudes = np.linspace((- 30), 30, 11)
    theta = np.deg2rad(random.uniform(magnitudes[magnitude], magnitudes[(magnitude + 1)]))
    transform_matrix = np.array([[np.cos(theta), (- np.sin(theta)), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    transform_matrix = transform_matrix_offset_center(transform_matrix, img.shape[0], img.shape[1])
    affine_matrix = transform_matrix[(:2, :2)]
    offset = transform_matrix[(:2, 2)]
    img = np.stack([ndimage.interpolation.affine_transform(img[(:, :, c)], affine_matrix, offset) for c in range(img.shape[2])], axis=2)
    img = Image.fromarray(img)
    return img

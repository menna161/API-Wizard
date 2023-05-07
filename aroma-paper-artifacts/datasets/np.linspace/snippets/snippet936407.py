import random
import numpy as np
import scipy
from scipy import ndimage
from PIL import Image, ImageEnhance, ImageOps


def translate_y(img, magnitude):
    img = np.array(img)
    magnitudes = np.linspace(((- 150) / 331), (150 / 331), 11)
    transform_matrix = np.array([[1, 0, (img.shape[0] * random.uniform(magnitudes[magnitude], magnitudes[(magnitude + 1)]))], [0, 1, 0], [0, 0, 1]])
    transform_matrix = transform_matrix_offset_center(transform_matrix, img.shape[0], img.shape[1])
    affine_matrix = transform_matrix[(:2, :2)]
    offset = transform_matrix[(:2, 2)]
    img = np.stack([ndimage.interpolation.affine_transform(img[(:, :, c)], affine_matrix, offset) for c in range(img.shape[2])], axis=2)
    img = Image.fromarray(img)
    return img

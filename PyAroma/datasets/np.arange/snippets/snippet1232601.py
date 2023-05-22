import numpy as np
from PIL import Image
from scipy.stats import multivariate_normal


def generate_glare_mask(mask_size, mean, cov, max_val, level):
    'Generate a glare mask from a 2-dimensional Gaussian.\n\n    Args:\n        mask_size (tuple): (width, height) of the mask to generate\n        mean (np.ndarray): (x, y) point about which Gaussian is centered\n        cov (np.ndarray): 2x2 matrix controlling spread of Gaussian\n        max_val (float): value to normalize values to before clamping\n        level (int): level of perturbation\n\n    Returns:\n        (Image): RGBA base mask of size mask_size\n\n    '
    (width, height) = mask_size
    mask = np.zeros((height, width, 4), dtype=float)
    mask[(:, :, :3)] = 255
    normal = multivariate_normal(mean=mean, cov=cov)
    (x_vals, y_vals) = np.meshgrid(np.arange(width), np.arange(height))
    vals = np.stack([x_vals, y_vals], axis=(- 1))
    alpha = normal.pdf(vals)
    mask[(:, :, 3)] = np.fmin((150 + (20 * level)), ((alpha * max_val) / np.max(alpha)))
    return Image.fromarray(np.uint8(mask))

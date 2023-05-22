import numpy as np
from PIL import Image
from scipy.stats import multivariate_normal


def glare(img, location, level):
    'Simulate a glare effect.\n\n    Generate semi-transparent white masks where opacity is determined by a\n    2-dimensional Gaussian. Masks are directly alpha-composited onto the\n    image.\n\n    Args:\n        img (Image): PIL image on which to apply the glare effect\n        mask_params (list): list of (mean, cov, max_val), which control\n            various aspects of mask appearance.\n            mean (np.ndarray): (x, y) point about which Gaussian is centered\n            cov (np.ndarray): 2x2 matrix controlling spread of Gaussian\n            max_val (float): value to normalize values to before clamping\n        level (int): level of perturbation\n\n    '
    img = img.convert('RGBA')
    (width, height) = img.size
    mask = np.zeros((height, width, 4), dtype=float)
    mask[(:, :, :3)] = 255
    mask[(:, :, 3)] = 0
    width_box = (((level * 0.1) * width) + (np.random.uniform(0, 0.05) * width))
    height_box = (((level * 0.1) * height) + (np.random.uniform(0, 0.05) * height))
    location = np.random.randint(1, 10)
    if (location == 1):
        mask[(:int(height_box), :int(width_box), 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 2):
        start_x = np.random.uniform(0.3, 0.7)
        x_start = int(((start_x * height) - (height_box / 2)))
        x_end = int(((start_x * height) + (height_box / 2)))
        mask[(x_start:x_end, :int(width_box), 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 3):
        mask[((height - int(height_box)):height, :int(width_box), 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 4):
        start_y = np.random.uniform(0.3, 0.7)
        y_start = int(((start_y * width) - (width_box / 2)))
        y_end = int(((start_y * width) + (width_box / 2)))
        mask[(:int(height_box), y_start:y_end, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 5):
        start_x = np.random.uniform(0.3, 0.7)
        x_start = int(((start_x * height) - (height_box / 2)))
        x_end = int(((start_x * height) + (height_box / 2)))
        start_y = np.random.uniform(0.3, 0.7)
        y_start = int(((start_y * width) - (width_box / 2)))
        y_end = int(((start_y * width) + (width_box / 2)))
        mask[(x_start:x_end, y_start:y_end, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 6):
        start_y = np.random.uniform(0.3, 0.7)
        y_start = int(((start_y * width) - (width_box / 2)))
        y_end = int(((start_y * width) + (width_box / 2)))
        mask[((height - int(height_box)):height, y_start:y_end, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 7):
        mask[(:int(height_box), (width - int(width_box)):width, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 8):
        start_x = np.random.uniform(0.3, 0.7)
        x_start = int(((start_x * height) - (height_box / 2)))
        x_end = int(((start_x * height) + (height_box / 2)))
        mask[(x_start:x_end, (width - int(width_box)):width, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    if (location == 9):
        mask[((height - int(height_box)):height, (width - int(width_box)):width, 3)] = ((150 + (20 * level)) + np.random.uniform(0, 20))
    mask = Image.fromarray(np.uint8(mask))
    img.alpha_composite(mask)
    img = img.convert('RGB')
    return img

import numpy as np
from PIL import Image
from scipy.stats import multivariate_normal


def glare_glossy_mapping(level, src_img):
    'Perform the glare matte mapping.\n\n    Args:\n        level (int): level of perturbation\n        src_img (Image): PIL Image to perturb\n\n    Returns:\n        (Image): the Image perturbed by the glare mapping\n\n    '
    (width, height) = src_img.size
    location = np.random.randint(1, 10)
    return glare(src_img, location, level)

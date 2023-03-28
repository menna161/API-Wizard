import cv2
import numpy as np


def contrast(image):
    '\n        Contrast distortion.\n        '
    (contrast_lower, contrast_upper) = contrast_range
    if rng.randint(2):
        return convert(image, alpha=rng.uniform(contrast_lower, contrast_upper))
    return image

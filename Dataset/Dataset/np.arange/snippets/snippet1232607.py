import numpy as np
from PIL import Image


def generate_base_mask(mask_size, thickness, gap, opacity, darkness):
    'Generate a base mask that can be later transformed.\n\n    The base mask consists of semi-transparent horizontal parallel lines\n    separated by fully transparent gaps.\n\n    Args:\n        mask_size (tuple): (width, height) of the mask to generate\n        thickness (int): width of mask lines in pixels\n        gap (int): gap between adjacent mask lines in pixels\n        opacity (float): opacity of mask lines in [0, 1]\n        darkness (float): darkness of mask lines in [0, 1]\n\n    Returns:\n        (Image): RGBA base mask of size mask_size\n\n    '
    (width, height) = mask_size
    mask = np.zeros((height, width, 4), dtype=np.uint8)
    remainders = np.remainder(np.arange(height), (thickness + gap))
    dark_rows = np.nonzero((remainders < thickness))
    light_rows = np.nonzero((remainders >= thickness))
    mask[(dark_rows, :, 3)] = int((opacity * 255))
    mask[(dark_rows, :, :3)] = int(((1 - darkness) * 255))
    return Image.fromarray(np.uint8(mask))

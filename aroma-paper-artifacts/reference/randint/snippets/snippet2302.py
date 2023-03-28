import numpy as np
from lib.config import cfg
from PIL import Image
import matplotlib.pyplot as plt


def image_transform(img, crop_x, crop_y, crop_loc=None, color_tint=None):
    '\n    Takes numpy.array img\n    '
    if (cfg.TRAIN.RANDOM_CROP and (not crop_loc)):
        crop_loc = [np.random.randint(0, crop_y), np.random.randint(0, crop_x)]
    if crop_loc:
        (cr, cc) = crop_loc
        (height, width, _) = img.shape
        img_h = (height - crop_y)
        img_w = (width - crop_x)
        img = img[cr:(cr + img_h), cc:(cc + img_w)]
    if (cfg.TRAIN.FLIP and (np.random.rand() > 0.5)):
        img = img[:, ::(- 1), ...]
    return img

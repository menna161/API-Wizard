import numpy as np
from lib.config import cfg
from PIL import Image
import matplotlib.pyplot as plt


def add_random_color_background(im, color_range):
    (r, g, b) = [np.random.randint(color_range[i][0], (color_range[i][1] + 1)) for i in range(3)]
    if isinstance(im, Image.Image):
        im = np.array(im)
    if (im.shape[2] > 3):
        alpha = (np.expand_dims(im[:, :, 3], axis=2) == 0).astype(np.float)
        im = im[:, :, :3]
        bg_color = np.array([[[r, g, b]]])
        im = ((alpha * bg_color) + ((1 - alpha) * im))
    return im

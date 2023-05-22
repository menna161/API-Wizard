import random
import numpy as np
import scipy
from scipy import ndimage
from PIL import Image, ImageEnhance, ImageOps


def cutout(org_img, magnitude=None):
    img = np.array(img)
    magnitudes = np.linspace(0, (60 / 331), 11)
    img = np.copy(org_img)
    mask_val = img.mean()
    if (magnitude is None):
        mask_size = 16
    else:
        mask_size = int(round((img.shape[0] * random.uniform(magnitudes[magnitude], magnitudes[(magnitude + 1)]))))
    top = np.random.randint((0 - (mask_size // 2)), (img.shape[0] - mask_size))
    left = np.random.randint((0 - (mask_size // 2)), (img.shape[1] - mask_size))
    bottom = (top + mask_size)
    right = (left + mask_size)
    if (top < 0):
        top = 0
    if (left < 0):
        left = 0
    img[(top:bottom, left:right, :)].fill(mask_val)
    img = Image.fromarray(img)
    return img

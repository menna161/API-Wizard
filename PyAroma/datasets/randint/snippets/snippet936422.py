import random
import numpy as np
import scipy
from scipy import ndimage
from PIL import Image, ImageEnhance, ImageOps


def __call__(self, img):
    img = np.array(img)
    mask_val = img.mean()
    top = np.random.randint((0 - (self.length // 2)), (img.shape[0] - self.length))
    left = np.random.randint((0 - (self.length // 2)), (img.shape[1] - self.length))
    bottom = (top + self.length)
    right = (left + self.length)
    top = (0 if (top < 0) else top)
    left = (0 if (left < 0) else top)
    img[(top:bottom, left:right, :)] = mask_val
    img = Image.fromarray(img)
    return img
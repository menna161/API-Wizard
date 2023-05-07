from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from random import randint


def __call__(self, img):
    factor = int((np.random.randn(1) * 8))
    factor = min(max(factor, (- 30)), 30)
    factor = np.array(factor, dtype=np.uint8)
    hsv = np.array(img.convert('HSV'))
    hsv[(:, :, 0)] += factor
    new_img = Image.fromarray(hsv, 'HSV').convert('RGB')
    return new_img

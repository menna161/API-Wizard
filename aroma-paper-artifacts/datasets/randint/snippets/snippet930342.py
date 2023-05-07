import os
from PIL import Image
import os.path
import time
import numpy as np
import PIL
from multiprocessing import Pool
import argparse
import skimage as sk
from skimage.filters import gaussian
from io import BytesIO
from wand.image import Image as WandImage
from wand.api import library as wandlibrary
import wand.color as WandColor
import ctypes
from PIL import Image as PILImage
import cv2
from scipy.ndimage import zoom as scizoom
from scipy.ndimage.interpolation import map_coordinates
import warnings
import collections


def glass_blur(x, severity=1):
    c = [(0.7, 1, 2), (0.9, 2, 1), (1, 2, 3), (1.1, 3, 2), (1.5, 4, 2)][(severity - 1)]
    x = np.uint8((gaussian((np.array(x) / 255.0), sigma=c[0], multichannel=True) * 255))
    for i in range(c[2]):
        for h in range((args.CROP_SIZE - c[1]), c[1], (- 1)):
            for w in range((args.CROP_SIZE - c[1]), c[1], (- 1)):
                (dx, dy) = np.random.randint((- c[1]), c[1], size=(2,))
                (h_prime, w_prime) = ((h + dy), (w + dx))
                (x[(h, w)], x[(h_prime, w_prime)]) = (x[(h_prime, w_prime)], x[(h, w)])
    return (np.clip(gaussian((x / 255.0), sigma=c[0], multichannel=True), 0, 1) * 255)

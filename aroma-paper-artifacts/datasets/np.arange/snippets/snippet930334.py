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


def disk(radius, alias_blur=0.1, dtype=np.float32):
    if (radius <= 8):
        L = np.arange((- 8), (8 + 1))
        ksize = (3, 3)
    else:
        L = np.arange((- radius), (radius + 1))
        ksize = (5, 5)
    (X, Y) = np.meshgrid(L, L)
    aliased_disk = np.array((((X ** 2) + (Y ** 2)) <= (radius ** 2)), dtype=dtype)
    aliased_disk /= np.sum(aliased_disk)
    return cv2.GaussianBlur(aliased_disk, ksize=ksize, sigmaX=alias_blur)
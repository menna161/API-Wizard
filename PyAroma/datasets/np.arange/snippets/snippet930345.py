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


def zoom_blur(x, severity=1):
    c = [np.arange(1, 1.11, 0.01), np.arange(1, 1.16, 0.01), np.arange(1, 1.21, 0.02), np.arange(1, 1.26, 0.02), np.arange(1, 1.31, 0.03)][(severity - 1)]
    x = (np.array(x) / 255.0).astype(np.float32)
    out = np.zeros_like(x)
    for zoom_factor in c:
        out += clipped_zoom(x, zoom_factor)
    x = ((x + out) / (len(c) + 1))
    return (np.clip(x, 0, 1) * 255)

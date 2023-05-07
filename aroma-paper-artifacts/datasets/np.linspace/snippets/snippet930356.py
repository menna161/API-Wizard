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


def split_range(total, num_split, start_index=0):
    rs = np.linspace(start_index, total, (num_split + 1)).astype(np.int)
    result = [[rs[i], rs[(i + 1)]] for i in range((len(rs) - 1))]
    return result

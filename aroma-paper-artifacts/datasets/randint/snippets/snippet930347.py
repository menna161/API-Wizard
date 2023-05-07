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


def frost(x, severity=1):
    c = [(1, 0.4), (0.8, 0.6), (0.7, 0.7), (0.65, 0.7), (0.6, 0.75)][(severity - 1)]
    idx = np.random.randint(5)
    filename = ['frost1.png', 'frost2.png', 'frost3.png', 'frost4.jpg', 'frost5.jpg', 'frost6.jpg'][idx]
    frost = cv2.imread(os.path.join(args.frost_dir, filename))
    (x_start, y_start) = (np.random.randint(0, (frost.shape[0] - args.CROP_SIZE)), np.random.randint(0, (frost.shape[1] - args.CROP_SIZE)))
    frost = frost[(x_start:(x_start + args.CROP_SIZE), y_start:(y_start + args.CROP_SIZE))][(..., [2, 1, 0])]
    return np.clip(((c[0] * np.array(x)) + (c[1] * frost)), 0, 255)

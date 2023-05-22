import colorsys
import pygame
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from skimage import transform as trans
import time
import math
import scipy
import cv2


def generate_ncolors(num_colors):
    color_pallet = []
    for i in range(0, 360, (360 / num_colors)):
        hue = i
        saturation = (90 + ((float(randint(0, 1000)) / 1000) * 10))
        lightness = (50 + ((float(randint(0, 1000)) / 1000) * 10))
        color = colorsys.hsv_to_rgb((float(hue) / 360.0), (saturation / 100), (lightness / 100))
        color_pallet.append(color)
    return color_pallet

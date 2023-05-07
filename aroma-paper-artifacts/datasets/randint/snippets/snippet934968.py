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


def draw_pt(img, x, y, color, sz=1):
    (row, col) = perspective_tform(x, y)
    if ((0 <= row < img.shape[0]) and (0 <= col < img.shape[1])):
        img[(int((row - sz)):int((row + sz)), int(((col - sz) - 65)):int(((col + sz) - 65)))] = color

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


def __init__(self, load_steer=False):
    pygame.init()
    self._render_iter = 2000
    self._speed_limit = 50.0
    if load_steer:
        self._wheel = cv2.imread('./drive_interfaces/wheel.png')
        self._wheel = cv2.resize(self._wheel, (int((0.08 * self._wheel.shape[0])), int((0.08 * self._wheel.shape[1]))))

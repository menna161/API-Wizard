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


def draw_path_on(img, speed_ms, angle_steers, color=(0, 0, 255)):
    path_x = np.arange(0.0, 50.1, 0.5)
    (path_y, _) = calc_lookahead_offset(speed_ms, angle_steers, path_x)
    draw_path(img, path_x, path_y, color)

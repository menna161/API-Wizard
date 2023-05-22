import cv2
import matplotlib
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np


def show_mask(mask):
    plt.figure(figsize=(10, 10))
    plt.imshow(mask, cmap='gray')

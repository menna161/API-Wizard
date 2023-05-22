import cv2
import matplotlib
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np


def show(image):
    plt.figure(figsize=(15, 15))
    plt.imshow(image, interpolation='nearest')
    plt.show()

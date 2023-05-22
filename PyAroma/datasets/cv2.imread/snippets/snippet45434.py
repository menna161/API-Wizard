import numpy as np
from os import listdir
from os.path import join, isdir
from glob import glob
import cv2
import timeit
import sys
from multiprocessing import Pool


def task(path):
    pixel_num = 0
    channel_sum = np.zeros(CHANNEL_NUM)
    channel_sum_squared = np.zeros(CHANNEL_NUM)
    print(('processing image ' + str(path)))
    im = cv2.imread(path)
    im = (im / 255.0)
    pixel_num += (im.size / CHANNEL_NUM)
    channel_sum += np.sum(im, axis=(0, 1))
    channel_sum_squared += np.sum(np.square(im), axis=(0, 1))
    return (pixel_num, channel_sum, channel_sum_squared)

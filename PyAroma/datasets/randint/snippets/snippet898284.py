import cv2
import numpy as np
import tensorflow as tf
from logging import exception
import math
import scipy.stats as st
import os
import urllib
import scipy
from scipy import io
from enum import Enum
from easydict import EasyDict as edict


def npmask(bbox, height, width, delta_h, delta_w):
    mask = np.zeros((1, height, width, 1), np.float32)
    h = np.random.randint(((delta_h // 2) + 1))
    w = np.random.randint(((delta_w // 2) + 1))
    mask[(:, (bbox[0] + h):((bbox[0] + bbox[2]) - h), (bbox[1] + w):((bbox[1] + bbox[3]) - w), :)] = 1.0
    return mask

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


def np_free_form_mask(maxVertex, maxLength, maxBrushWidth, maxAngle, h, w):
    mask = np.zeros((h, w, 1), np.float32)
    numVertex = np.random.randint((maxVertex + 1))
    startY = np.random.randint(h)
    startX = np.random.randint(w)
    brushWidth = 0
    for i in range(numVertex):
        angle = np.random.randint((maxAngle + 1))
        angle = (((angle / 360.0) * 2) * np.pi)
        if ((i % 2) == 0):
            angle = ((2 * np.pi) - angle)
        length = np.random.randint((maxLength + 1))
        brushWidth = ((np.random.randint(10, (maxBrushWidth + 1)) // 2) * 2)
        nextY = (startY + (length * np.cos(angle)))
        nextX = (startX + (length * np.sin(angle)))
        nextY = np.maximum(np.minimum(nextY, (h - 1)), 0).astype(np.int)
        nextX = np.maximum(np.minimum(nextX, (w - 1)), 0).astype(np.int)
        cv2.line(mask, (startY, startX), (nextY, nextX), 1, brushWidth)
        cv2.circle(mask, (startY, startX), (brushWidth // 2), 2)
        (startY, startX) = (nextY, nextX)
    cv2.circle(mask, (startY, startX), (brushWidth // 2), 2)
    return mask

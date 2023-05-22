import os
import time
import cv2
import torch
import numpy as np
import torch.utils.data as data


@staticmethod
def _open_image(filepath, mode=cv2.IMREAD_COLOR, dtype=None):
    img = np.array(cv2.imread(filepath, mode), dtype=dtype)
    return img

import numpy as np
import cv2
import math
import time
import shutil
import os, re
import tensorflow as tf
from net.ops import np_free_form_mask


def generate_mask_rect(im_shapes, mask_shapes, rand=True):
    mask = np.zeros((im_shapes[0], im_shapes[1])).astype(np.float32)
    if rand:
        of0 = np.random.randint(0, (im_shapes[0] - mask_shapes[0]))
        of1 = np.random.randint(0, (im_shapes[1] - mask_shapes[1]))
    else:
        of0 = ((im_shapes[0] - mask_shapes[0]) // 2)
        of1 = ((im_shapes[1] - mask_shapes[1]) // 2)
    mask[(of0:(of0 + mask_shapes[0]), of1:(of1 + mask_shapes[1]))] = 1
    mask = np.expand_dims(mask, axis=2)
    return mask

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import argparse
import glob
import cv2
import numpy as np
import pickle
import random
import collections
from time import time
from tensorflow.python.client import device_lib


def LoadDataByID(root, index):
    color_src_img = (root + ('/%05d_color.png' % index))
    uv_src_img = (root + ('/%05d_uv.npz' % index))
    depth_src_img = (root + ('/%05d_depth.npz' % index))
    mask_src_img = (root + ('/%05d_mask.png' % index))
    pose = (root + ('/%05d_pose.txt' % index))
    color_src = (cv2.imread(color_src_img) / 255.0)
    uv_src = np.load(uv_src_img)['arr_0']
    depth_src = np.load(depth_src_img)['arr_0']
    mask_src = (cv2.imread(mask_src_img, cv2.IMREAD_UNCHANGED) / 255.0)
    world2cam = np.loadtxt(pose)
    return (color_src.astype('float32'), uv_src.astype('float32'), depth_src.astype('float32'), mask_src.astype('float32'), world2cam.astype('float32'))

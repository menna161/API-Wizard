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


def crop_quarters(feature_tensor):
    (N, fH, fW, fC) = feature_tensor.shape.as_list()
    quarters_list = []
    quarter_size = [N, round((fH / 2)), round((fW / 2)), fC]
    quarters_list.append(tf.slice(feature_tensor, [0, 0, 0, 0], quarter_size))
    quarters_list.append(tf.slice(feature_tensor, [0, round((fH / 2)), 0, 0], quarter_size))
    quarters_list.append(tf.slice(feature_tensor, [0, 0, round((fW / 2)), 0], quarter_size))
    quarters_list.append(tf.slice(feature_tensor, [0, round((fH / 2)), round((fW / 2)), 0], quarter_size))
    feature_tensor = tf.concat(quarters_list, axis=0)
    return feature_tensor

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import argparse
import json
import glob
import random
import collections
import math
import time
from lxml import etree
from random import shuffle


def reshape_tensor_display(tensor, splitAmount, logAlbedo=False):
    tensors_list = tf.split(tensor, splitAmount, axis=3)
    if logAlbedo:
        tensors_list[(- 1)] = logTensor(tensors_list[(- 1)])
        tensors_list[1] = logTensor(tensors_list[1])
    tensors = tf.stack(tensors_list, axis=1)
    shape = tf.shape(tensors)
    newShape = tf.concat([[(shape[0] * shape[1])], shape[2:]], axis=0)
    tensors_reshaped = tf.reshape(tensors, newShape)
    return tensors_reshaped

import os
import random
import datetime
import re
import math
import logging
from collections import OrderedDict
import multiprocessing
import numpy as np
import skimage.transform
import tensorflow as tf
import keras
import keras.backend as K
import keras.layers as KL
import keras.engine as KE
import keras.models as KM
from keras.callbacks import Callback
from mrcnn import utils
from distutils.version import LooseVersion
import imgaug
import h5py
from keras.engine import topology
from keras.utils.data_utils import get_file
from mrcnn.parallel_model import ParallelModel


def bottom_up_agg(Ps):
    (P2, P3, P4, P5) = Ps
    N2 = P2
    N3 = KL.Add()([P3, KL.Conv2D(256, (3, 3), strides=(2, 2), padding='SAME')(N2)])
    N3 = KL.Conv2D(256, (3, 3), padding='SAME')(N3)
    N4 = KL.Add()([P4, KL.Conv2D(256, (3, 3), strides=(2, 2), padding='SAME')(N3)])
    N4 = KL.Conv2D(256, (3, 3), padding='SAME')(N4)
    N5 = KL.Add()([P5, KL.Conv2D(256, (3, 3), strides=(2, 2), padding='SAME')(N4)])
    N5 = KL.Conv2D(256, (3, 3), padding='SAME')(N5)
    return [N2, N3, N4, N5]

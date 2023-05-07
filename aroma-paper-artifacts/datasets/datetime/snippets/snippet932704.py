from __future__ import division
import math
import os
import datetime
import pprint
import scipy.misc
import numpy as np
import pretty_midi as pm
import copy
import config
import write_midi
import tensorflow as tf
from imageio import imread as _imread


def center_crop(x, crop_h, crop_w, resize_h=64, resize_w=64):
    if (crop_w is None):
        crop_w = crop_h
    (h, w) = x.shape[:2]
    j = int(round(((h - crop_h) / 2.0)))
    i = int(round(((w - crop_w) / 2.0)))
    return scipy.misc.imresize(x[(j:(j + crop_h), i:(i + crop_w))], [resize_h, resize_w])

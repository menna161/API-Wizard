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


def get_now_datetime():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return str(now)

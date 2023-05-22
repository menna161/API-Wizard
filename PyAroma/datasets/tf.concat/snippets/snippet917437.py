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


def tf_generate_normalized_random_direction(batchSize, lowEps=0.001, highEps=0.05):
    r1 = tf.random_uniform([batchSize, 1], (0.0 + lowEps), (1.0 - highEps), dtype=tf.float32)
    r2 = tf.random_uniform([batchSize, 1], 0.0, 1.0, dtype=tf.float32)
    r = tf.sqrt(r1)
    phi = ((2 * math.pi) * r2)
    x = (r * tf.cos(phi))
    y = (r * tf.sin(phi))
    z = tf.sqrt((1.0 - tf.square(r)))
    finalVec = tf.concat([x, y, z], axis=(- 1))
    return finalVec

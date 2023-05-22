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


def tf_generateSpecularRendering(batchSize, surfaceArray, targets, outputs):
    currentViewDir = tf_generate_normalized_random_direction(batchSize)
    currentLightDir = (currentViewDir * tf.expand_dims([(- 1.0), (- 1.0), 1.0], axis=0))
    currentShift = tf.concat([tf.random_uniform([batchSize, 2], (- 1.0), 1.0), (tf.zeros([batchSize, 1], dtype=tf.float32) + 0.0001)], axis=(- 1))
    currentViewPos = (tf.multiply(currentViewDir, tf_generate_distance(batchSize)) + currentShift)
    currentLightPos = (tf.multiply(currentLightDir, tf_generate_distance(batchSize)) + currentShift)
    currentViewPos = tf.expand_dims(currentViewPos, axis=1)
    currentViewPos = tf.expand_dims(currentViewPos, axis=1)
    currentLightPos = tf.expand_dims(currentLightPos, axis=1)
    currentLightPos = tf.expand_dims(currentLightPos, axis=1)
    wo = (currentViewPos - surfaceArray)
    wi = (currentLightPos - surfaceArray)
    renderedSpecular = tf_Render(targets, wi, wo, includeDiffuse=a.includeDiffuse)
    renderedSpecularOutputs = tf_Render(outputs, wi, wo, includeDiffuse=a.includeDiffuse)
    return [renderedSpecular, renderedSpecularOutputs]

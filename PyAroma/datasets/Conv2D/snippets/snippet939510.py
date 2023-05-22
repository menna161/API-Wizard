import argparse
import numpy as np
import os
import multiprocessing as mp
import tensorflow as tf
from tensorpack import *
from tensorpack.utils import logger
from tensorpack.tfutils.tower import TowerFunc
from tensorpack.tfutils.varreplace import custom_getter_scope
from tensorpack.dataflow import dataset


def residual(name, x, chan):
    with tf.variable_scope(name):
        x = Conv2D('res1', x, chan, 3)
        x = BatchNorm('bn1', x)
        x = activation(x)
        x = Conv2D('res2', x, chan, 3)
        x = BatchNorm('bn2', x)
        x = activation(x)
        return x

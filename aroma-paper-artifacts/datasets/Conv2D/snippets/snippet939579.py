import sys
import argparse
import os
from contextlib import contextmanager, ExitStack
import tensorflow as tf
from tensorpack import *
from tensorpack.utils.gpu import get_nr_gpu
from tensorpack.tfutils.summary import *
from tensorpack.utils.argtools import log_once
from tensorpack.tfutils.collection import freeze_collection
from tensorpack.tfutils import get_current_tower_context
from tensorpack.tfutils.varreplace import custom_getter_scope
from tfbench.convnet_builder import ConvNetBuilder
from tfbench import model_config
from tensorpack.callbacks import ThroughputTracker


def shortcut(l, n_in, n_out, stride):
    if (n_in != n_out):
        l = Conv2D('convshortcut', l, n_out, 1, strides=stride)
        l = BatchNorm('bnshortcut', l)
        return l
    else:
        return l

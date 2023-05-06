import argparse
import math
from datetime import datetime
import h5py
import numpy as np
import tensorflow as tf
import socket
import importlib
import os
import sys
import provider
import tf_util
import modelnet_dataset
import modelnet_h5_dataset


def average_gradients(tower_grads):
    'Calculate the average gradient for each shared variable across all towers.\n  Note that this function provides a synchronization point across all towers.\n  From tensorflow tutorial: cifar10/cifar10_multi_gpu_train.py\n  Args:\n    tower_grads: List of lists of (gradient, variable) tuples. The outer list\n      is over individual gradients. The inner list is over the gradient\n      calculation for each tower.\n  Returns:\n     List of pairs of (gradient, variable) where the gradient has been averaged\n     across all towers.\n  '
    average_grads = []
    for grad_and_vars in zip(*tower_grads):
        grads = []
        for (g, v) in grad_and_vars:
            expanded_g = tf.expand_dims(g, 0)
            grads.append(expanded_g)
        grad = tf.concat(axis=0, values=grads)
        grad = tf.reduce_mean(grad, 0)
        v = grad_and_vars[0][1]
        grad_and_var = (grad, v)
        average_grads.append(grad_and_var)
    return average_grads

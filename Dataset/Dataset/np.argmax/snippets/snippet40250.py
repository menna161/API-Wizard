import tensorflow as tf
import numpy as np
import argparse
import socket
import importlib
import time
import os
import scipy.misc
import sys
import provider
import show3d_balls
import part_dataset
import matplotlib.pyplot as plt


def inference(sess, ops, pc, batch_size):
    ' pc: BxNx3 array, return BxN pred '
    assert ((pc.shape[0] % batch_size) == 0)
    num_batches = (pc.shape[0] / batch_size)
    logits = np.zeros((pc.shape[0], pc.shape[1], NUM_CLASSES))
    for i in range(num_batches):
        feed_dict = {ops['pointclouds_pl']: pc[((i * batch_size):((i + 1) * batch_size), ...)], ops['is_training_pl']: False}
        batch_logits = sess.run(ops['pred'], feed_dict=feed_dict)
        logits[((i * batch_size):((i + 1) * batch_size), ...)] = batch_logits
    return np.argmax(logits, 2)

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


def train_one_epoch(sess, ops, train_writer):
    ' ops: dict mapping from string to tf ops '
    is_training = True
    log_string(str(datetime.now()))
    cur_batch_data = np.zeros((BATCH_SIZE, NUM_POINT, TRAIN_DATASET.num_channel()))
    cur_batch_label = np.zeros(BATCH_SIZE, dtype=np.int32)
    total_correct = 0
    total_seen = 0
    loss_sum = 0
    batch_idx = 0
    while TRAIN_DATASET.has_next_batch():
        (batch_data, batch_label) = TRAIN_DATASET.next_batch(augment=True)
        bsize = batch_data.shape[0]
        cur_batch_data[(0:bsize, ...)] = batch_data
        cur_batch_label[0:bsize] = batch_label
        feed_dict = {ops['pointclouds_pl']: cur_batch_data, ops['labels_pl']: cur_batch_label, ops['is_training_pl']: is_training}
        (summary, step, _, loss_val, pred_val) = sess.run([ops['merged'], ops['step'], ops['train_op'], ops['loss'], ops['pred']], feed_dict=feed_dict)
        train_writer.add_summary(summary, step)
        pred_val = np.argmax(pred_val, 1)
        correct = np.sum((pred_val[0:bsize] == batch_label[0:bsize]))
        total_correct += correct
        total_seen += bsize
        loss_sum += loss_val
        if (((batch_idx + 1) % 50) == 0):
            log_string((' ---- batch: %03d ----' % (batch_idx + 1)))
            log_string(('mean loss: %f' % (loss_sum / 50)))
            log_string(('accuracy: %f' % (total_correct / float(total_seen))))
            total_correct = 0
            total_seen = 0
            loss_sum = 0
        batch_idx += 1
    TRAIN_DATASET.reset()

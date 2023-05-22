import argparse
import math
from datetime import datetime
import numpy as np
import tensorflow as tf
import importlib
import os
import sys
import provider
import tf_util
import pc_util
import dfc_dataset


def train_one_epoch(sess, ops, train_writer):
    ' ops: dict mapping from string to tf ops '
    is_training = True
    train_idxs = np.arange(0, len(TRAIN_DATASET))
    np.random.shuffle(train_idxs)
    num_batches = int(math.ceil(((1.0 * len(TRAIN_DATASET)) / BATCH_SIZE)))
    log_string(str(datetime.now()))
    total_correct = 0
    total_seen = 0
    loss_sum = 0
    for batch_idx in range(num_batches):
        start_idx = (batch_idx * BATCH_SIZE)
        end_idx = ((batch_idx + 1) * BATCH_SIZE)
        (batch_data, batch_label, batch_smpw) = get_batch_wdp(TRAIN_DATASET, train_idxs, start_idx, end_idx)
        if FLAGS.extra_dims:
            aug_data = np.concatenate((provider.rotate_point_cloud_z(batch_data[(:, :, 0:3)]), batch_data[(:, :, 3:)]), axis=2)
        else:
            aug_data = provider.rotate_point_cloud_z(batch_data)
        feed_dict = {ops['pointclouds_pl']: aug_data, ops['labels_pl']: batch_label, ops['smpws_pl']: batch_smpw, ops['is_training_pl']: is_training}
        (summary, step, _, loss_val, pred_val) = sess.run([ops['merged'], ops['step'], ops['train_op'], ops['loss'], ops['pred']], feed_dict=feed_dict)
        train_writer.add_summary(summary, step)
        pred_val = np.argmax(pred_val, 2)
        correct = np.sum((pred_val == batch_label))
        total_correct += correct
        total_seen += (BATCH_SIZE * NUM_POINT)
        loss_sum += loss_val
        if (((batch_idx + 1) % 10) == 0):
            log_string((' -- %03d / %03d --' % ((batch_idx + 1), num_batches)))
            log_string(('mean loss: %f' % (loss_sum / 10)))
            log_string(('accuracy: %f' % (total_correct / float(total_seen))))
            total_correct = 0
            total_seen = 0
            loss_sum = 0

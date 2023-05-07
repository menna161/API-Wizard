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


def eval_one_epoch(sess, ops, test_writer):
    ' ops: dict mapping from string to tf ops '
    global EPOCH_CNT
    is_training = False
    cur_batch_data = np.zeros((BATCH_SIZE, NUM_POINT, TEST_DATASET.num_channel()))
    cur_batch_label = np.zeros(BATCH_SIZE, dtype=np.int32)
    total_correct = 0
    total_seen = 0
    loss_sum = 0
    batch_idx = 0
    shape_ious = []
    total_seen_class = [0 for _ in range(NUM_CLASSES)]
    total_correct_class = [0 for _ in range(NUM_CLASSES)]
    log_string(str(datetime.now()))
    log_string(('---- EPOCH %03d EVALUATION ----' % EPOCH_CNT))
    while TEST_DATASET.has_next_batch():
        (batch_data, batch_label) = TEST_DATASET.next_batch(augment=False)
        bsize = batch_data.shape[0]
        cur_batch_data[(0:bsize, ...)] = batch_data
        cur_batch_label[0:bsize] = batch_label
        feed_dict = {ops['pointclouds_pl']: cur_batch_data, ops['labels_pl']: cur_batch_label, ops['is_training_pl']: is_training}
        (summary, step, loss_val, pred_val) = sess.run([ops['merged'], ops['step'], ops['loss'], ops['pred']], feed_dict=feed_dict)
        test_writer.add_summary(summary, step)
        pred_val = np.argmax(pred_val, 1)
        correct = np.sum((pred_val[0:bsize] == batch_label[0:bsize]))
        total_correct += correct
        total_seen += bsize
        loss_sum += loss_val
        batch_idx += 1
        for i in range(0, bsize):
            l = batch_label[i]
            total_seen_class[l] += 1
            total_correct_class[l] += (pred_val[i] == l)
    log_string(('eval mean loss: %f' % (loss_sum / float(batch_idx))))
    log_string(('eval accuracy: %f' % (total_correct / float(total_seen))))
    log_string(('eval avg class acc: %f' % np.mean((np.array(total_correct_class) / np.array(total_seen_class, dtype=np.float)))))
    EPOCH_CNT += 1
    TEST_DATASET.reset()
    return (total_correct / float(total_seen))

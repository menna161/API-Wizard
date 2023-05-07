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


def eval_one_epoch(sess, ops, test_writer):
    ' ops: dict mapping from string to tf ops '
    is_training = False
    test_idxs = np.arange(0, len(TEST_DATASET))
    num_batches = int(math.ceil(((1.0 * len(TEST_DATASET)) / BATCH_SIZE)))
    total_correct = 0
    total_seen = 0
    loss_sum = 0
    total_seen_class = [0 for _ in range(NUM_CLASSES)]
    total_correct_class = [0 for _ in range(NUM_CLASSES)]
    labelweights = np.zeros(NUM_CLASSES)
    tp = np.zeros(NUM_CLASSES)
    fp = np.zeros(NUM_CLASSES)
    fn = np.zeros(NUM_CLASSES)
    for batch_idx in range(num_batches):
        start_idx = (batch_idx * BATCH_SIZE)
        end_idx = ((batch_idx + 1) * BATCH_SIZE)
        (batch_data, batch_label, batch_smpw) = get_batch(TEST_DATASET, test_idxs, start_idx, end_idx)
        if FLAGS.extra_dims:
            aug_data = np.concatenate((provider.rotate_point_cloud_z(batch_data[(:, :, 0:3)]), batch_data[(:, :, 3:)]), axis=2)
        else:
            aug_data = provider.rotate_point_cloud_z(batch_data)
        feed_dict = {ops['pointclouds_pl']: aug_data, ops['labels_pl']: batch_label, ops['smpws_pl']: batch_smpw, ops['is_training_pl']: is_training}
        (summary, step, loss_val, pred_val) = sess.run([ops['merged'], ops['step'], ops['loss'], ops['pred']], feed_dict=feed_dict)
        test_writer.add_summary(summary, step)
        pred_val = np.argmax(pred_val, 2)
        correct = np.sum((((pred_val == batch_label) & (batch_label > 0)) & (batch_smpw > 0)))
        total_correct += correct
        total_seen += np.sum(((batch_label > 0) & (batch_smpw > 0)))
        loss_sum += loss_val
        for l in range(NUM_CLASSES):
            total_seen_class[l] += np.sum(((batch_label == l) & (batch_smpw > 0)))
            total_correct_class[l] += np.sum((((pred_val == l) & (batch_label == l)) & (batch_smpw > 0)))
            tp[l] += ((pred_val == l) & (batch_label == l)).sum()
            fp[l] += ((pred_val == l) & (batch_label != l)).sum()
            fn[l] += ((pred_val != l) & (batch_label == l)).sum()
    log_string(('eval mean loss: %f' % (loss_sum / float(num_batches))))
    log_string(('eval point accuracy: %f' % (total_correct / float(total_seen))))
    log_string(('eval point avg class acc: %f' % np.mean((np.array(total_correct_class) / (np.array(total_seen_class, dtype=np.float) + 1e-06)))))
    per_class_str = '     '
    iou = np.divide(tp, ((tp + fp) + fn))
    for l in range(NUM_CLASSES):
        per_class_str += ('class %d[%d] acc: %f, iou: %f; ' % (TEST_DATASET.decompress_label_map[l], l, (total_correct_class[l] / float(total_seen_class[l])), iou[l]))
    log_string(per_class_str)
    log_string('mIOU: {}'.format(iou.mean()))
    return (total_correct / float(total_seen))

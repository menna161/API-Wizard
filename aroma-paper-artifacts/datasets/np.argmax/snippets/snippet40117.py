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
import modelnet_dataset
import modelnet_h5_dataset


def eval_one_epoch(sess, ops, num_votes=1, topk=1):
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
    while TEST_DATASET.has_next_batch():
        (batch_data, batch_label) = TEST_DATASET.next_batch(augment=False)
        bsize = batch_data.shape[0]
        print(('Batch: %03d, batch size: %d' % (batch_idx, bsize)))
        cur_batch_data[(0:bsize, ...)] = batch_data
        cur_batch_label[0:bsize] = batch_label
        batch_pred_sum = np.zeros((BATCH_SIZE, NUM_CLASSES))
        for vote_idx in range(num_votes):
            shuffled_indices = np.arange(NUM_POINT)
            np.random.shuffle(shuffled_indices)
            if FLAGS.normal:
                rotated_data = provider.rotate_point_cloud_by_angle_with_normal(cur_batch_data[(:, shuffled_indices, :)], (((vote_idx / float(num_votes)) * np.pi) * 2))
            else:
                rotated_data = provider.rotate_point_cloud_by_angle(cur_batch_data[(:, shuffled_indices, :)], (((vote_idx / float(num_votes)) * np.pi) * 2))
            feed_dict = {ops['pointclouds_pl']: rotated_data, ops['labels_pl']: cur_batch_label, ops['is_training_pl']: is_training}
            (loss_val, pred_val) = sess.run([ops['loss'], ops['pred']], feed_dict=feed_dict)
            batch_pred_sum += pred_val
        pred_val = np.argmax(batch_pred_sum, 1)
        correct = np.sum((pred_val[0:bsize] == batch_label[0:bsize]))
        total_correct += correct
        total_seen += bsize
        loss_sum += loss_val
        batch_idx += 1
        for i in range(bsize):
            l = batch_label[i]
            total_seen_class[l] += 1
            total_correct_class[l] += (pred_val[i] == l)
    log_string(('eval mean loss: %f' % (loss_sum / float(batch_idx))))
    log_string(('eval accuracy: %f' % (total_correct / float(total_seen))))
    log_string(('eval avg class acc: %f' % np.mean((np.array(total_correct_class) / np.array(total_seen_class, dtype=np.float)))))
    class_accuracies = (np.array(total_correct_class) / np.array(total_seen_class, dtype=np.float))
    for (i, name) in enumerate(SHAPE_NAMES):
        log_string(('%10s:\t%0.3f' % (name, class_accuracies[i])))

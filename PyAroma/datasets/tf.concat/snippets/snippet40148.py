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


def train():
    with tf.Graph().as_default():
        with tf.device('/cpu:0'):
            (pointclouds_pl, labels_pl) = MODEL.placeholder_inputs(BATCH_SIZE, NUM_POINT)
            is_training_pl = tf.placeholder(tf.bool, shape=())
            batch = tf.get_variable('batch', [], initializer=tf.constant_initializer(0), trainable=False)
            bn_decay = get_bn_decay(batch)
            tf.summary.scalar('bn_decay', bn_decay)
            learning_rate = get_learning_rate(batch)
            tf.summary.scalar('learning_rate', learning_rate)
            if (OPTIMIZER == 'momentum'):
                optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=MOMENTUM)
            elif (OPTIMIZER == 'adam'):
                optimizer = tf.train.AdamOptimizer(learning_rate)
            MODEL.get_model(pointclouds_pl, is_training_pl, bn_decay=bn_decay)
            tower_grads = []
            pred_gpu = []
            total_loss_gpu = []
            for i in range(NUM_GPUS):
                with tf.variable_scope(tf.get_variable_scope(), reuse=True):
                    with tf.device(('/gpu:%d' % i)), tf.name_scope(('gpu_%d' % i)) as scope:
                        pc_batch = tf.slice(pointclouds_pl, [(i * DEVICE_BATCH_SIZE), 0, 0], [DEVICE_BATCH_SIZE, (- 1), (- 1)])
                        label_batch = tf.slice(labels_pl, [(i * DEVICE_BATCH_SIZE)], [DEVICE_BATCH_SIZE])
                        (pred, end_points) = MODEL.get_model(pc_batch, is_training=is_training_pl, bn_decay=bn_decay)
                        MODEL.get_loss(pred, label_batch, end_points)
                        losses = tf.get_collection('losses', scope)
                        total_loss = tf.add_n(losses, name='total_loss')
                        for l in (losses + [total_loss]):
                            tf.summary.scalar(l.op.name, l)
                        grads = optimizer.compute_gradients(total_loss)
                        tower_grads.append(grads)
                        pred_gpu.append(pred)
                        total_loss_gpu.append(total_loss)
            pred = tf.concat(pred_gpu, 0)
            total_loss = tf.reduce_mean(total_loss_gpu)
            grads = average_gradients(tower_grads)
            train_op = optimizer.apply_gradients(grads, global_step=batch)
            correct = tf.equal(tf.argmax(pred, 1), tf.to_int64(labels_pl))
            accuracy = (tf.reduce_sum(tf.cast(correct, tf.float32)) / float(BATCH_SIZE))
            tf.summary.scalar('accuracy', accuracy)
        saver = tf.train.Saver()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        config.log_device_placement = False
        sess = tf.Session(config=config)
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(os.path.join(LOG_DIR, 'train'), sess.graph)
        test_writer = tf.summary.FileWriter(os.path.join(LOG_DIR, 'test'), sess.graph)
        init = tf.global_variables_initializer()
        sess.run(init)
        ops = {'pointclouds_pl': pointclouds_pl, 'labels_pl': labels_pl, 'is_training_pl': is_training_pl, 'pred': pred, 'loss': total_loss, 'train_op': train_op, 'merged': merged, 'step': batch, 'end_points': end_points}
        best_acc = (- 1)
        for epoch in range(MAX_EPOCH):
            log_string(('**** EPOCH %03d ****' % epoch))
            sys.stdout.flush()
            train_one_epoch(sess, ops, train_writer)
            eval_one_epoch(sess, ops, test_writer)
            if ((epoch % 10) == 0):
                save_path = saver.save(sess, os.path.join(LOG_DIR, 'model.ckpt'))
                log_string(('Model saved in file: %s' % save_path))

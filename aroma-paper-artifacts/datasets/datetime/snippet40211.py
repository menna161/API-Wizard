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


def train():
    with tf.Graph().as_default():
        with tf.device(('/device:GPU:' + str(GPU_INDEX))):
            (pointclouds_pl, labels_pl, smpws_pl) = MODEL.placeholder_inputs(BATCH_SIZE, NUM_POINT)
            is_training_pl = tf.placeholder(tf.bool, shape=())
            print(is_training_pl)
            batch = tf.Variable(0)
            bn_decay = get_bn_decay(batch)
            tf.summary.scalar('bn_decay', bn_decay)
            print('--- Get model and loss')
            (pred, end_points) = MODEL.get_model(pointclouds_pl, is_training_pl, NUM_CLASSES, bn_decay=bn_decay)
            loss = MODEL.get_loss(pred, labels_pl, smpws_pl)
            tf.summary.scalar('loss', loss)
            pred_class = tf.argmax(pred, 2)
            true_class = tf.to_int64(labels_pl)
            correct = tf.equal(pred_class, true_class)
            accuracy = (tf.reduce_sum(tf.cast(correct, tf.float32)) / float((BATCH_SIZE * NUM_POINT)))
            tf.summary.scalar('accuracy', accuracy)
            for l in range(NUM_CLASSES):
                a = tf.equal(pred_class, tf.to_int64(l))
                b = tf.equal(true_class, tf.to_int64(l))
                A = tf.reduce_sum(tf.cast(tf.logical_and(a, b), tf.float32))
                B = tf.reduce_sum(tf.cast(tf.logical_or(a, b), tf.float32))
                iou = tf.divide(A, B)
                if (l == 0):
                    miou = iou
                else:
                    miou += iou
                tf.summary.scalar('iou_{}'.format(l), iou)
            miou = tf.divide(miou, tf.to_float(NUM_CLASSES))
            tf.summary.scalar('mIOU', miou)
            print('--- Get training operator')
            learning_rate = get_learning_rate(batch)
            tf.summary.scalar('learning_rate', learning_rate)
            if (OPTIMIZER == 'momentum'):
                optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=MOMENTUM)
            elif (OPTIMIZER == 'adam'):
                optimizer = tf.train.AdamOptimizer(learning_rate)
            train_op = optimizer.minimize(loss, global_step=batch)
            saver = tf.train.Saver(max_to_keep=5, keep_checkpoint_every_n_hours=1)
            bestsaver = tf.train.Saver()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        config.log_device_placement = False
        sess = tf.Session(config=config)
        if FLAGS.existing_model:
            log_string(('Loading model from ' + FLAGS.existing_model))
            saver.restore(sess, FLAGS.existing_model)
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(os.path.join(LOG_DIR, 'train'), sess.graph)
        test_writer = tf.summary.FileWriter(os.path.join(LOG_DIR, 'test'), sess.graph)
        if (not FLAGS.existing_model):
            init = tf.global_variables_initializer()
            sess.run(init)
        ops = {'pointclouds_pl': pointclouds_pl, 'labels_pl': labels_pl, 'smpws_pl': smpws_pl, 'is_training_pl': is_training_pl, 'pred': pred, 'loss': loss, 'train_op': train_op, 'merged': merged, 'step': batch, 'end_points': end_points}
        best_acc = (- 1)
        for epoch in range(FLAGS.starting_epoch, MAX_EPOCH):
            log_string(('**** EPOCH %03d ****' % epoch))
            sys.stdout.flush()
            train_one_epoch(sess, ops, train_writer)
            do_save = ((epoch % 10) == 0)
            if ((epoch % 5) == 0):
                log_string(str(datetime.now()))
                log_string(('---- EPOCH %03d EVALUATION ----' % epoch))
                acc = eval_one_epoch(sess, ops, test_writer)
                if (acc > best_acc):
                    best_acc = acc
                    save_path = bestsaver.save(sess, os.path.join(LOG_DIR, 'best_model.ckpt'), global_step=(epoch * len(TRAIN_DATASET)))
                    log_string(('Model saved in file: %s' % save_path))
                    do_save = False
            if do_save:
                save_path = saver.save(sess, os.path.join(LOG_DIR, 'model.ckpt'), global_step=(epoch * len(TRAIN_DATASET)))
                log_string(('Model saved in file: %s' % save_path))

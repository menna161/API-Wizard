import argparse
import copy
from datetime import datetime
from enum import Enum
import glob
import importlib
import json
import logging
import math
import numpy as np
import os
import pickle
from pointset import PointSet
import pprint
from queue import Queue
import subprocess
import sys
import tempfile
import tensorflow as tf
import threading
import provider
import tf_util
import pc_util


def main_processor(input_queue, output_queue):
    with tf.Graph().as_default():
        with tf.device(('/device:GPU:' + str(GPU_INDEX))):
            (pointclouds_pl, labels_pl, smpws_pl) = MODEL.placeholder_inputs(BATCH_SIZE, NUM_POINT)
            is_training_pl = tf.placeholder(tf.bool, shape=())
            logging.info('Loading model')
            (pred, end_points) = MODEL.get_model(pointclouds_pl, is_training_pl, NUM_CLASSES)
            saver = tf.train.Saver()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        sess = tf.Session(config=config)
        saver.restore(sess, MODEL_PATH)
        ops = {'pointclouds_pl': pointclouds_pl, 'is_training_pl': is_training_pl, 'pred': pred}
        is_training = False
        logging.info('Model loaded')
        while True:
            in_data = input_queue.get()
            if (in_data is None):
                break
            logging.info('Processing {}'.format(in_data[0].filename))
            batch_list = in_data[1]
            for k in range(len(batch_list)):
                batch_raw = batch_list[k][0]
                aug_data = batch_list[k][1]
                feed_dict = {ops['pointclouds_pl']: aug_data, ops['is_training_pl']: is_training}
                pred_val = sess.run([ops['pred']], feed_dict=feed_dict)
                pred_labels = np.argmax(pred_val[0], 2)
                if (batch_raw.shape[0] != BATCH_SIZE):
                    pred_labels = pred_labels[(0:batch_raw.shape[0], :)]
                pred_labels.shape = (pred_labels.shape[0] * pred_labels.shape[1])
                batch_raw.shape = ((batch_raw.shape[0] * batch_raw.shape[1]), batch_raw.shape[2])
                if (k == 0):
                    all_labels = pred_labels
                    all_points = batch_raw
                else:
                    all_labels = np.concatenate((all_labels, pred_labels), axis=0)
                    all_points = np.concatenate((all_points, batch_raw), axis=0)
            logging.debug('Adding {} to output queue'.format(in_data[0].filename))
            output_queue.put((in_data[0], all_points, all_labels))
            logging.debug('Added {} to output queue'.format(in_data[0].filename))
            input_queue.task_done()
        logging.info('Main processing finished')
        output_queue.put(None)
    logging.debug('Main processing thread finished')

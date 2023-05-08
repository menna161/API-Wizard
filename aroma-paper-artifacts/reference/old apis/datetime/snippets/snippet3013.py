import os, sys
import tensorflow as tf
import numpy as np
import argparse
import pprint
import importlib
import datetime
import time
import dataset.maps_dict as maps_dict
from tensorflow.python import pywrap_tensorflow
from tensorflow.python.client import device_lib as _device_lib
from core.config import cfg, cfg_from_file, cfg_from_list, assert_and_infer_cfg
from core.trainer_utils import *
from dataset.dataloader import choose_dataset
from dataset.feeddict_builder import FeedDictCreater
from modeling import choose_model


def __init__(self, args):
    self.batch_size = cfg.TRAIN.CONFIG.BATCH_SIZE
    self.gpu_num = cfg.TRAIN.CONFIG.GPU_NUM
    self.num_workers = cfg.DATA_LOADER.NUM_THREADS
    self.log_dir = cfg.MODEL.PATH.CHECKPOINT_DIR
    self.max_iteration = cfg.TRAIN.CONFIG.MAX_ITERATIONS
    self.checkpoint_interval = cfg.TRAIN.CONFIG.CHECKPOINT_INTERVAL
    self.summary_interval = cfg.TRAIN.CONFIG.SUMMARY_INTERVAL
    self.trainable_param_prefix = cfg.TRAIN.CONFIG.TRAIN_PARAM_PREFIX
    self.trainable_loss_prefix = cfg.TRAIN.CONFIG.TRAIN_LOSS_PREFIX
    self.restore_model_path = args.restore_model_path
    self.is_training = True
    self.gpu_num = min(self.gpu_num, len(self._get_available_gpu_num()))
    datetime_str = str(datetime.datetime.now())
    self.log_dir = os.path.join(self.log_dir, datetime_str)
    if (not os.path.exists(self.log_dir)):
        os.makedirs(self.log_dir)
    self.log_file = open(os.path.join(self.log_dir, 'log_train.txt'), 'w')
    self.log_file.write((str(args) + '\n'))
    self._log_string(('**** Saving models to the path %s ****' % self.log_dir))
    self._log_string(('**** Saving configure file in %s ****' % self.log_dir))
    os.system(('cp "%s" "%s"' % (args.cfg, self.log_dir)))
    dataset_func = choose_dataset()
    self.dataset = dataset_func('loading', split=args.split, img_list=args.img_list, is_training=self.is_training, workers_num=self.num_workers)
    self.dataset_iter = self.dataset.load_batch((self.batch_size * self.gpu_num))
    self._log_string(('**** Dataset length is %d ****' % len(self.dataset)))
    with tf.device('/cpu:0'):
        self.global_step = tf.contrib.framework.get_or_create_global_step()
        self.bn_decay = get_bn_decay(self.global_step)
        self.learning_rate = get_learning_rate(self.global_step)
        if (cfg.SOLVER.TYPE == 'SGD'):
            self.optimizer = tf.train.MomentumOptimizer(self.learning_rate, momentum=cfg.SOLVER.MOMENTUM)
        elif (cfg.SOLVER.TYPE == 'Adam'):
            self.optimizer = tf.train.AdamOptimizer(self.learning_rate)
    self.model_func = choose_model()
    (self.model_list, self.tower_grads, self.total_loss_gpu, self.losses_list, self.params, self.extra_update_ops) = self._build_model_list()
    tf.summary.scalar('total_loss', self.total_loss_gpu)
    self.feeddict_producer = FeedDictCreater(self.dataset_iter, self.model_list, self.batch_size)
    with tf.device('/gpu:0'):
        self.grads = average_gradients(self.tower_grads)
        self.update_op = [self.optimizer.apply_gradients(zip(self.grads, self.params), global_step=self.global_step)]
    self.update_op.extend(self.extra_update_ops)
    self.train_op = tf.group(*self.update_op)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1, allow_growth=True)
    config = tf.ConfigProto(gpu_options=gpu_options, device_count={'GPU': self.gpu_num}, allow_soft_placement=True)
    self.sess = tf.Session(config=config)
    self.saver = tf.train.Saver()
    self.merged = tf.summary.merge_all()
    self.train_writer = tf.summary.FileWriter(os.path.join(self.log_dir, 'train'), self.sess.graph)
    self._initialize_model()

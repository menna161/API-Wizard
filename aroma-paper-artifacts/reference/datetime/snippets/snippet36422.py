import sys
import os
import platform
import argparse
import datetime
import numpy as np
import tensorflow as tf
import provider
import copy
import models.tp8 as MODEL_tp8
from config import load_config, configGlobal, save_config
import logging
from tqdm import tqdm as tqdm_orig
import evaluation
import icp
import time
from pointcloud import get_mat_angle
from scipy.spatial.transform import Rotation
from tensorflow.python import pywrap_tensorflow
import matplotlib


def train(eval_only=False, eval_epoch=None, eval_only_model_to_load=None, do_timings=False, override_batch_size=None):
    with tf.Graph().as_default():
        with tf.device(('/gpu:' + str(cfg.gpu_index))):
            (pcs1, pcs2, translations, rel_angles, pc1centers, pc2centers, pc1angles, pc2angles) = MODEL.placeholder_inputs(cfg.training.batch_size, cfg.model.num_points)
            is_training_pl = tf.placeholder(tf.bool, shape=())
            batch = tf.Variable(0)
            bn_decay = get_bn_decay(batch)
            tf.summary.scalar('hyperparameters/bn_decay', bn_decay)
            end_points = MODEL.get_model(pcs1, pcs2, is_training_pl, bn_decay=bn_decay)
            loss = MODEL.get_loss(pcs1, pcs2, translations, rel_angles, pc1centers, pc2centers, pc1angles, pc2angles, end_points)
            tf.summary.scalar('losses/loss', loss)
            learning_rate = get_learning_rate(batch)
            tf.summary.scalar('hyperparameters/learning_rate', learning_rate)
            if (cfg.training.optimizer.optimizer == 'momentum'):
                optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=cfg.training.optimizer.momentum)
            elif (cfg.training.optimizer.optimizer == 'adam'):
                optimizer = tf.train.AdamOptimizer(learning_rate)
            else:
                assert False, 'Invalid optimizer'
            train_op = optimizer.minimize(loss, global_step=batch)
            saver = tf.train.Saver(max_to_keep=1000)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        config.log_device_placement = False
        sess = tf.Session(config=config)
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(os.path.join(cfg.logging.logdir, 'train'), sess.graph)
        val_writer = tf.summary.FileWriter(os.path.join(cfg.logging.logdir, 'val'))
        val_writer_180 = tf.summary.FileWriter(os.path.join(cfg.logging.logdir, 'val_180'))
        init = tf.global_variables_initializer()
        sess.run(init, {is_training_pl: True})
        ops = {'pcs1': pcs1, 'pcs2': pcs2, 'translations': translations, 'rel_angles': rel_angles, 'is_training_pl': is_training_pl, 'pred_translations': end_points['pred_translations'], 'pred_remaining_angle_logits': end_points['pred_remaining_angle_logits'], 'pc1centers': pc1centers, 'pc2centers': pc2centers, 'pc1angles': pc1angles, 'pc2angles': pc2angles, 'pred_s1_pc1centers': end_points['pred_s1_pc1centers'], 'pred_s1_pc2centers': end_points['pred_s1_pc2centers'], 'pred_s2_pc1centers': end_points['pred_s2_pc1centers'], 'pred_s2_pc2centers': end_points['pred_s2_pc2centers'], 'pred_pc1angle_logits': end_points['pred_pc1angle_logits'], 'pred_pc2angle_logits': end_points['pred_pc2angle_logits'], 'loss': loss, 'train_op': train_op, 'merged': merged, 'step': batch}
        start_epoch = 0
        if eval_only:
            model_to_load = cfg.logging.logdir
            if (eval_only_model_to_load is not None):
                model_to_load = eval_only_model_to_load
            if ((not FLAGS.use_old_results) and (not do_timings)):
                assert os.path.isfile(f'{model_to_load}/model-{eval_epoch}.index'), f'{model_to_load}/model-{eval_epoch}.index'
                saver.restore(sess, f'{model_to_load}/model-{eval_epoch}')
            start_epoch = int(eval_epoch)
            if (eval_only_model_to_load is None):
                num_batches_per_epoch = (len(TRAIN_INDICES) // cfg.training.batch_size)
                if (FLAGS.use_old_results or do_timings):
                    start_epoch = int(eval_epoch)
                else:
                    restored_batch = sess.run(batch)
                    assert ((restored_batch % num_batches_per_epoch) == 0)
                    start_epoch = ((restored_batch // num_batches_per_epoch) - 1)
                    assert (start_epoch == int(eval_epoch))
            logger.info(f'Evaluating at epoch {start_epoch}')
        elif os.path.isfile(os.path.join(cfg.logging.logdir, 'model.ckpt.index')):
            saver.restore(sess, os.path.join(cfg.logging.logdir, 'model.ckpt'))
            num_batches_per_epoch = (len(TRAIN_INDICES) // cfg.training.batch_size)
            restored_batch = sess.run(batch)
            assert ((restored_batch % num_batches_per_epoch) == 0)
            start_epoch = (restored_batch // num_batches_per_epoch)
            logger.info(f'Continuing training at epoch {start_epoch}')
        elif (cfg.training.pretraining.model != ''):
            assert os.path.isfile((cfg.training.pretraining.model + '.index'))
            variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
            variables_to_load = [var for var in variables if (var not in [batch])]
            saverPretraining = tf.train.Saver(variables_to_load)
            saverPretraining.restore(sess, cfg.training.pretraining.model)
            restored_batch = sess.run(batch)
            assert (restored_batch == 0)
            logger.info(f'Pre-trained weights loaded from {cfg.training.pretraining.model}, starting initial evaluation')
            (lr, bn_d) = sess.run([learning_rate, bn_decay])
            eval_one_epoch(sess, ops, val_writer, val_writer_180, 'pretr', eval_only=False, do_timings=False)
            logger.info(f'Initial evaluation finished')
        try:
            start = time.time()
            for epoch in range(start_epoch, cfg.training.num_epochs):
                (lr, bn_d) = sess.run([learning_rate, bn_decay])
                logger.info((('**** EPOCH %03d ****    ' % epoch) + f'lr: {lr:.8f}, bn_decay: {bn_d:.8f}'))
                if (not eval_only):
                    train_one_epoch(sess, ops, train_writer, epoch)
                if (eval_only or True or ((epoch % 10) == 0)):
                    if do_timings:
                        for i in range(10):
                            eval_one_epoch(sess, ops, val_writer, val_writer_180, epoch, eval_only=eval_only, do_timings=True, override_batch_size=override_batch_size)
                    else:
                        eval_one_epoch(sess, ops, val_writer, val_writer_180, epoch, eval_only=eval_only, do_timings=False)
                if eval_only:
                    break
                if (not eval_only):
                    was_last_epoch = (epoch == (cfg.training.num_epochs - 1))
                    if (((epoch % 2) == 0) or was_last_epoch):
                        save_path = saver.save(sess, os.path.join(cfg.logging.logdir, 'model.ckpt'))
                        logger.info(('Model saved in file: %s' % save_path))
                    if (((epoch % 5) == 0) or was_last_epoch or cfg.evaluation.save_every_epoch):
                        save_path = saver.save(sess, os.path.join(cfg.logging.logdir, 'model'), global_step=epoch)
                        logger.info(('Model saved in file: %s' % save_path))
                now = time.time()
                time_elapsed = (now - start)
                time_elapsed_str = str(datetime.timedelta(seconds=time_elapsed))
                time_remaining = ((time_elapsed / (epoch + 1)) * ((cfg.training.num_epochs - epoch) - 1))
                time_remaining_str = str(datetime.timedelta(seconds=time_remaining))
                logger.info(f'Finished epoch {epoch}. Time elapsed: {time_elapsed_str}, Time remaining: {time_remaining_str}')
            logger.info('Finished Training')
        except KeyboardInterrupt:
            logger.info('Interrupted')

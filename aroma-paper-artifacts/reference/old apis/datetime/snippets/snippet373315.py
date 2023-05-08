import logging
import colorlog
import tensorflow as tf
from model.model import CSMN
from utils.data_utils import enqueue
from utils.configuration import ModelConfig
from datetime import datetime
import time
import numpy as np
import os


def train():
    colorlog.basicConfig(filename=None, level=logging.INFO, format='%(log_color)s[%(levelname)s:%(asctime)s]%(reset)s %(message)s', datafmt='%Y-%m-%d %H:%M:%S')
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.95)
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=False, gpu_options=gpu_options)) as sess:
        global_step = tf.get_variable('global_step', [], initializer=tf.constant_initializer(0), trainable=False)
        (num_examples_per_epoch, tower_img_embedding, tower_context_length, tower_caption_length, tower_context_id, tower_caption_id, tower_answer_id, tower_context_mask, tower_caption_mask) = enqueue(False)
        num_batches_per_epoch = ((num_examples_per_epoch / FLAGS.batch_size) / FLAGS.num_gpus)
        decay_steps = int((num_batches_per_epoch * NUM_EPOCHS_PER_DECAY))
        lr = tf.train.exponential_decay(FLAGS.init_lr, global_step, decay_steps, LEARNING_RATE_DECAY_FACTOR, staircase=True)
        opt = tf.train.AdamOptimizer(lr)
        tower_grads = []
        with tf.variable_scope(tf.get_variable_scope()) as scope:
            for i in xrange(FLAGS.num_gpus):
                with tf.device(('/gpu:%d' % i)):
                    with tf.name_scope(('%s_%d' % (TOWER_NAME, i))) as scope:
                        inputs = [tower_img_embedding[i], tower_context_length[i], tower_caption_length[i], tower_context_id[i], tower_caption_id[i], tower_answer_id[i], tower_context_mask[i], tower_caption_mask[i]]
                        loss = _tower_loss(inputs, scope)
                        tf.get_variable_scope().reuse_variables()
                        summaries = tf.get_collection(tf.GraphKeys.SUMMARIES, scope)
                        grads = opt.compute_gradients(loss)
                        tower_grads.append(grads)
        grads = _average_gradients(tower_grads)
        summaries.append(tf.summary.scalar('learning_rate', lr))
        clipped_grads_and_vars = [(tf.clip_by_norm(gv[0], FLAGS.max_grad_norm), gv[1]) for gv in grads]
        apply_gradient_op = opt.apply_gradients(clipped_grads_and_vars, global_step=global_step)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=200)
        summary_op = tf.summary.merge(summaries)
        init = tf.global_variables_initializer()
        sess.run(init)
        ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
        if (ckpt and ckpt.model_checkpoint_path):
            saver.restore(sess, ckpt.model_checkpoint_path)
        tf.train.start_queue_runners(sess=sess)
        summary_writer = tf.summary.FileWriter(FLAGS.train_dir, sess.graph)
        for step in xrange(FLAGS.max_steps):
            start_time = time.time()
            (_, loss_value) = sess.run([apply_gradient_op, loss])
            duration = (time.time() - start_time)
            assert (not np.isnan(loss_value)), 'Model diverged with loss = NaN'
            if (((step + 1) % 10) == 0):
                num_examples_per_step = (FLAGS.batch_size * FLAGS.num_gpus)
                examples_per_sec = (num_examples_per_step / duration)
                sec_per_batch = (duration / FLAGS.num_gpus)
                format_str = '%s: step %d, loss = %.2f (%.1f examples/sec; %.3f sec/batch)'
                c_g_step = int(global_step.eval(session=sess))
                print((format_str % (datetime.now(), c_g_step, loss_value, examples_per_sec, sec_per_batch)))
            if (((step + 1) % 25) == 0):
                summary_str = sess.run(summary_op)
                summary_writer.add_summary(summary_str, c_g_step)
            if ((((step + 1) % 500) == 0) or ((step + 1) == FLAGS.max_steps)):
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=c_g_step)

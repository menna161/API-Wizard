import datetime
import os
import tensorflow as tf
import time
from avod.builders import optimizer_builder
from avod.core import trainer_utils
from avod.core import summary_utils


def train(model, train_config):
    'Training function for detection models.\n\n    Args:\n        model: The detection model object.\n        train_config: a train_*pb2 protobuf.\n            training i.e. loading RPN weights onto AVOD model.\n    '
    model = model
    train_config = train_config
    model_config = model.model_config
    global_step_tensor = tf.Variable(0, trainable=False, name='global_step')
    max_iterations = train_config.max_iterations
    summary_interval = train_config.summary_interval
    checkpoint_interval = train_config.checkpoint_interval
    max_checkpoints = train_config.max_checkpoints_to_keep
    paths_config = model_config.paths_config
    logdir = paths_config.logdir
    if (not os.path.exists(logdir)):
        os.makedirs(logdir)
    checkpoint_dir = paths_config.checkpoint_dir
    if (not os.path.exists(checkpoint_dir)):
        os.makedirs(checkpoint_dir)
    checkpoint_path = ((checkpoint_dir + '/') + model_config.checkpoint_name)
    global_summaries = set([])
    prediction_dict = model.build()
    summary_histograms = train_config.summary_histograms
    summary_img_images = train_config.summary_img_images
    summary_bev_images = train_config.summary_bev_images
    (losses_dict, total_loss) = model.loss(prediction_dict)
    training_optimizer = optimizer_builder.build(train_config.optimizer, global_summaries, global_step_tensor)
    with tf.variable_scope('train_op'):
        train_op = slim.learning.create_train_op(total_loss, training_optimizer, clip_gradient_norm=1.0, global_step=global_step_tensor)
    saver = tf.train.Saver(max_to_keep=max_checkpoints, pad_step_number=True)
    tf.summary.scalar('training_loss', train_op)
    is_travis = ('TRAVIS' in os.environ)
    if (not is_travis):
        tf.summary.scalar('max_bytes', tf.contrib.memory_stats.MaxBytesInUse())
    summaries = set(tf.get_collection(tf.GraphKeys.SUMMARIES))
    summary_merged = summary_utils.summaries_to_keep(summaries, global_summaries, histograms=summary_histograms, input_imgs=summary_img_images, input_bevs=summary_bev_images)
    allow_gpu_mem_growth = train_config.allow_gpu_mem_growth
    if allow_gpu_mem_growth:
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = allow_gpu_mem_growth
        sess = tf.Session(config=config)
    else:
        sess = tf.Session()
    datetime_str = str(datetime.datetime.now())
    logdir = (logdir + '/train')
    train_writer = tf.summary.FileWriter(((logdir + '/') + datetime_str), sess.graph)
    init = tf.global_variables_initializer()
    if (not train_config.overwrite_checkpoints):
        trainer_utils.load_checkpoints(checkpoint_dir, saver)
        if (len(saver.last_checkpoints) > 0):
            checkpoint_to_restore = saver.last_checkpoints[(- 1)]
            saver.restore(sess, checkpoint_to_restore)
        else:
            sess.run(init)
    else:
        sess.run(init)
    global_step = tf.train.global_step(sess, global_step_tensor)
    print('Starting from step {} / {}'.format(global_step, max_iterations))
    last_time = time.time()
    for step in range(global_step, (max_iterations + 1)):
        if ((step % checkpoint_interval) == 0):
            global_step = tf.train.global_step(sess, global_step_tensor)
            saver.save(sess, save_path=checkpoint_path, global_step=global_step)
            print('Step {} / {}, Checkpoint saved to {}-{:08d}'.format(step, max_iterations, checkpoint_path, global_step))
        feed_dict = model.create_feed_dict()
        if ((step % summary_interval) == 0):
            current_time = time.time()
            time_elapsed = (current_time - last_time)
            last_time = current_time
            (train_op_loss, summary_out) = sess.run([train_op, summary_merged], feed_dict=feed_dict)
            print('Step {}, Total Loss {:0.3f}, Time Elapsed {:0.3f} s'.format(step, train_op_loss, time_elapsed))
            train_writer.add_summary(summary_out, step)
        else:
            sess.run(train_op, feed_dict)
    train_writer.close()

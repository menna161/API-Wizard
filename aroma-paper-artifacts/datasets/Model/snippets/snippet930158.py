from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
from absl import flags
import tensorflow as tf
import numpy as np
import glob
from functions import model_fns
from preprocessing import imagenet_preprocessing
import threading


def show_corruption_error_by_distortion(distortion_name, current_ckpt, gpu_id):
    synsets2idx = get_synsets2idx(FLAGS.label_file)
    distortion_dir = os.path.join(FLAGS.data_dir, distortion_name)
    with tf.device(('/gpu:%d' % gpu_id)):
        model = model_fns.Model(resnet_size=FLAGS.resnet_size, num_classes=FLAGS.num_classes, resnet_version=FLAGS.resnet_version, use_se_block=FLAGS.use_se_block, use_sk_block=FLAGS.use_sk_block, zero_gamma=FLAGS.zero_gamma, data_format=FLAGS.data_format, no_downsample=FLAGS.no_downsample, anti_alias_filter_size=FLAGS.anti_alias_filter_size, anti_alias_type=FLAGS.anti_alias_type, embedding_size=FLAGS.embedding_size, pool_type=FLAGS.pool_type, bl_alpha=FLAGS.bl_alpha, bl_beta=FLAGS.bl_beta, dtype=tf.float32)
        images = tf.placeholder(tf.float32, [None, FLAGS.image_size, FLAGS.image_size, 3])
        logits = model(inputs=images, training=False, use_resnet_d=FLAGS.use_resnet_d, reuse=tf.AUTO_REUSE)
        softmax = tf.nn.softmax(logits)
        sm_top1 = tf.nn.top_k(softmax, 1)
    saver = tf.train.Saver()
    image_files = []
    for severity in range(1, 6):
        severity_dir = os.path.join(distortion_dir, str(severity))
        for d in os.listdir(severity_dir):
            for f in glob.glob((os.path.join(severity_dir, d) + '/*')):
                image_files.append(f)
    dataset = input_fn_imagenet_c(image_files, FLAGS.batch_size)
    iterator = dataset.make_one_shot_iterator()
    next_element = iterator.get_next()
    with tf.Session() as sess:
        saver.restore(sess, current_ckpt)
        num_of_images = 0
        correct = 0
        while True:
            try:
                (images_tensor, image_files) = next_element
                (images_input, image_files) = sess.run([images_tensor, image_files])
                result = sess.run(sm_top1, feed_dict={images: images_input})
                for i in range(len(result.indices)):
                    fn = os.path.splitext(image_files[i].decode('utf-8'))[0]
                    synset = os.path.basename(os.path.dirname(fn))
                    gt = (synsets2idx[synset] + FLAGS.label_offset)
                    pred = result.indices[i][0]
                    num_of_images += 1
                    if (pred == gt):
                        correct += 1
            except tf.errors.OutOfRangeError:
                break
    assert (num_of_images > 0)
    err = (1 - ((1.0 * correct) / num_of_images))
    return err

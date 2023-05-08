from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import collections
from datetime import datetime
import hashlib
import os.path
import random
import re
import sys
import tarfile
import numpy as np
from six.moves import urllib
import tensorflow.compat.v1 as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile
from tensorflow.python.util import compat


def main(_):
    tf.logging.set_verbosity(tf.logging.INFO)
    prepare_file_system()
    model_info = create_model_info(FLAGS.architecture)
    if (not model_info):
        tf.logging.error('Did not recognize architecture flag')
        return (- 1)
    maybe_download_and_extract(model_info['data_url'])
    (graph, bottleneck_tensor, resized_image_tensor) = create_model_graph(model_info)
    image_lists = create_image_lists(FLAGS.image_dir, FLAGS.testing_percentage, FLAGS.validation_percentage)
    class_count = len(image_lists.keys())
    if (class_count == 0):
        tf.logging.error(('No valid folders of images found at ' + FLAGS.image_dir))
        return (- 1)
    if (class_count == 1):
        tf.logging.error((('Only one valid folder of images found at ' + FLAGS.image_dir) + ' - multiple classes are needed for classification.'))
        return (- 1)
    do_distort_images = should_distort_images(FLAGS.flip_left_right, FLAGS.random_crop, FLAGS.random_scale, FLAGS.random_brightness)
    with tf.Session(graph=graph) as sess:
        (jpeg_data_tensor, decoded_image_tensor) = add_jpeg_decoding(model_info['input_width'], model_info['input_height'], model_info['input_depth'], model_info['input_mean'], model_info['input_std'])
        if do_distort_images:
            (distorted_jpeg_data_tensor, distorted_image_tensor) = add_input_distortions(FLAGS.flip_left_right, FLAGS.random_crop, FLAGS.random_scale, FLAGS.random_brightness, model_info['input_width'], model_info['input_height'], model_info['input_depth'], model_info['input_mean'], model_info['input_std'])
        else:
            cache_bottlenecks(sess, image_lists, FLAGS.image_dir, FLAGS.bottleneck_dir, jpeg_data_tensor, decoded_image_tensor, resized_image_tensor, bottleneck_tensor, FLAGS.architecture)
        (train_step, cross_entropy, bottleneck_input, ground_truth_input, final_tensor) = add_final_training_ops(len(image_lists.keys()), FLAGS.final_tensor_name, bottleneck_tensor, model_info['bottleneck_tensor_size'])
        (evaluation_step, prediction) = add_evaluation_step(final_tensor, ground_truth_input)
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/train'), sess.graph)
        validation_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/validation'))
        init = tf.global_variables_initializer()
        sess.run(init)
        for i in range(FLAGS.how_many_training_steps):
            if do_distort_images:
                (train_bottlenecks, train_ground_truth) = get_random_distorted_bottlenecks(sess, image_lists, FLAGS.train_batch_size, 'training', FLAGS.image_dir, distorted_jpeg_data_tensor, distorted_image_tensor, resized_image_tensor, bottleneck_tensor)
            else:
                (train_bottlenecks, train_ground_truth, _) = get_random_cached_bottlenecks(sess, image_lists, FLAGS.train_batch_size, 'training', FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor, decoded_image_tensor, resized_image_tensor, bottleneck_tensor, FLAGS.architecture)
            (train_summary, _) = sess.run([merged, train_step], feed_dict={bottleneck_input: train_bottlenecks, ground_truth_input: train_ground_truth})
            train_writer.add_summary(train_summary, i)
            is_last_step = ((i + 1) == FLAGS.how_many_training_steps)
            if (((i % FLAGS.eval_step_interval) == 0) or is_last_step):
                (train_accuracy, cross_entropy_value) = sess.run([evaluation_step, cross_entropy], feed_dict={bottleneck_input: train_bottlenecks, ground_truth_input: train_ground_truth})
                tf.logging.info(('%s: Step %d: Train accuracy = %.1f%%' % (datetime.now(), i, (train_accuracy * 100))))
                tf.logging.info(('%s: Step %d: Cross entropy = %f' % (datetime.now(), i, cross_entropy_value)))
                (validation_bottlenecks, validation_ground_truth, _) = get_random_cached_bottlenecks(sess, image_lists, FLAGS.validation_batch_size, 'validation', FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor, decoded_image_tensor, resized_image_tensor, bottleneck_tensor, FLAGS.architecture)
                (validation_summary, validation_accuracy) = sess.run([merged, evaluation_step], feed_dict={bottleneck_input: validation_bottlenecks, ground_truth_input: validation_ground_truth})
                validation_writer.add_summary(validation_summary, i)
                tf.logging.info(('%s: Step %d: Validation accuracy = %.1f%% (N=%d)' % (datetime.now(), i, (validation_accuracy * 100), len(validation_bottlenecks))))
            intermediate_frequency = FLAGS.intermediate_store_frequency
            if ((intermediate_frequency > 0) and ((i % intermediate_frequency) == 0) and (i > 0)):
                intermediate_file_name = (((FLAGS.intermediate_output_graphs_dir + 'intermediate_') + str(i)) + '.pb')
                tf.logging.info(('Save intermediate result to : ' + intermediate_file_name))
                save_graph_to_file(sess, graph, intermediate_file_name)
        (test_bottlenecks, test_ground_truth, test_filenames) = get_random_cached_bottlenecks(sess, image_lists, FLAGS.test_batch_size, 'testing', FLAGS.bottleneck_dir, FLAGS.image_dir, jpeg_data_tensor, decoded_image_tensor, resized_image_tensor, bottleneck_tensor, FLAGS.architecture)
        (test_accuracy, predictions) = sess.run([evaluation_step, prediction], feed_dict={bottleneck_input: test_bottlenecks, ground_truth_input: test_ground_truth})
        tf.logging.info(('Final test accuracy = %.1f%% (N=%d)' % ((test_accuracy * 100), len(test_bottlenecks))))
        if FLAGS.print_misclassified_test_images:
            tf.logging.info('=== MISCLASSIFIED TEST IMAGES ===')
            for (i, test_filename) in enumerate(test_filenames):
                if (predictions[i] != test_ground_truth[i].argmax()):
                    tf.logging.info(('%70s  %s' % (test_filename, list(image_lists.keys())[predictions[i]])))
        save_graph_to_file(sess, graph, FLAGS.output_graph)
        with gfile.FastGFile(FLAGS.output_labels, 'w') as f:
            f.write(('\n'.join(image_lists.keys()) + '\n'))

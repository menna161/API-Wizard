from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import os
import tensorflow as tf
from official.utils.export import export
from utils import data_util
from functions import data_config
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import normalize


def export_test(bin_export_path, flags_obj, ir_eval):
    ds = tf.data.Dataset.list_files(((flags_obj.data_dir + '/') + flags_obj.val_regex))
    ds = ds.interleave(tf.data.TFRecordDataset, cycle_length=10)

    def parse_tfr(example_proto):
        feature_def = {'image/class/label': tf.FixedLenFeature([], dtype=tf.int64, default_value=(- 1)), 'image/encoded': tf.FixedLenFeature([], dtype=tf.string, default_value='')}
        features = tf.io.parse_single_example(serialized=example_proto, features=feature_def)
        return (features['image/encoded'], features['image/class/label'])
    ds = ds.map(parse_tfr)
    ds = ds.batch(flags_obj.val_batch_size)
    iterator = ds.make_one_shot_iterator()
    (images, labels) = iterator.get_next()
    dconf = data_config.get_config(flags_obj.dataset_name)
    num_val_images = dconf.num_images['validation']
    if (flags_obj.zeroshot_eval or ir_eval):
        feature_dim = (flags_obj.embedding_size if (flags_obj.embedding_size > 0) else flags_obj.num_features)
        np_features = np.zeros((num_val_images, feature_dim), dtype=np.float32)
        np_labels = np.zeros(num_val_images, dtype=np.int64)
        np_i = 0
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            tf.saved_model.load(sess=sess, export_dir=bin_export_path, tags={'serve'})
            for _ in tqdm(range((int((num_val_images / flags_obj.val_batch_size)) + 1))):
                try:
                    (np_image, np_label) = sess.run([images, labels])
                    np_predict = sess.run('embedding_tensor:0', feed_dict={'input_tensor:0': np_image})
                    np_features[(np_i:(np_i + np_predict.shape[0]), :)] = np_predict
                    np_labels[np_i:(np_i + np_label.shape[0])] = np_label
                    np_i += np_predict.shape[0]
                except tf.errors.OutOfRangeError:
                    break
            assert (np_i == num_val_images)
        from sklearn.preprocessing import normalize
        x = normalize(np_features)
        np_sim = x.dot(x.T)
        np.fill_diagonal(np_sim, (- 10))
        num_correct = 0
        for i in range(num_val_images):
            cur_label = np_labels[i]
            rank1_label = np_labels[np.argmax(np_sim[(i, :)])]
            if (rank1_label == cur_label):
                num_correct += 1
        recall_at_1 = (num_correct / num_val_images)
        metric = recall_at_1
    else:
        np_i = 0
        correct_cnt = 0
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            tf.saved_model.load(sess=sess, export_dir=bin_export_path, tags={'serve'})
            for _ in tqdm(range((int((num_val_images / flags_obj.val_batch_size)) + 1))):
                try:
                    (np_image, np_label) = sess.run([images, labels])
                    np_predict = sess.run('ArgMax:0', feed_dict={'input_tensor:0': np_image})
                    np_i += np_predict.shape[0]
                    correct_cnt += np.sum((np_predict == np_label))
                except tf.errors.OutOfRangeError:
                    break
            assert (np_i == num_val_images)
            metric = (correct_cnt / np_i)
    return metric

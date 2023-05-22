from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import operator
import numpy as np
import tensorflow as tf


def get_inference_input(inputs, params):
    with tf.device('/cpu:0'):
        dataset = tf.data.Dataset.from_tensor_slices(tf.constant(inputs))
        dataset = dataset.map((lambda x: tf.string_split([x]).values), num_parallel_calls=params.num_threads)
        dataset = dataset.map((lambda x: tf.concat([x, [tf.constant(params.eos)]], axis=0)), num_parallel_calls=params.num_threads)
        dataset = dataset.map((lambda x: {'source': x, 'source_length': tf.shape(x)[0]}), num_parallel_calls=params.num_threads)
        dataset = dataset.padded_batch((params.decode_batch_size * len(params.device_list)), {'source': [tf.Dimension(None)], 'source_length': []}, {'source': params.pad, 'source_length': 0})
        iterator = dataset.make_one_shot_iterator()
        features = iterator.get_next()
        src_table = tf.contrib.lookup.index_table_from_tensor(tf.constant(params.vocabulary['source']), default_value=params.mapping['source'][params.unk])
        features['source'] = src_table.lookup(features['source'])
        return features

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import operator
import numpy as np
import tensorflow as tf


def get_evaluation_input(inputs, params):
    with tf.device('/cpu:0'):
        datasets = []
        for data in inputs:
            dataset = tf.data.Dataset.from_tensor_slices(data)
            dataset = dataset.map((lambda x: tf.string_split([x]).values), num_parallel_calls=params.num_threads)
            dataset = dataset.map((lambda x: tf.concat([x, [tf.constant(params.eos)]], axis=0)), num_parallel_calls=params.num_threads)
            datasets.append(dataset)
        dataset = tf.data.Dataset.zip(tuple(datasets))
        dataset = dataset.map((lambda *x: {'source': x[0], 'source_length': tf.shape(x[0])[0], 'references': x[1:]}), num_parallel_calls=params.num_threads)
        dataset = dataset.padded_batch(params.eval_batch_size, {'source': [tf.Dimension(None)], 'source_length': [], 'references': ((tf.Dimension(None),) * (len(inputs) - 1))}, {'source': params.pad, 'source_length': 0, 'references': ((params.pad,) * (len(inputs) - 1))})
        iterator = dataset.make_one_shot_iterator()
        features = iterator.get_next()
        src_table = tf.contrib.lookup.index_table_from_tensor(tf.constant(params.vocabulary['source']), default_value=params.mapping['source'][params.unk])
        features['source'] = src_table.lookup(features['source'])
    return features

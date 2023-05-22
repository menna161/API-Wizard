from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import operator
import numpy as np
import tensorflow as tf


def get_training_input(filenames, params):
    ' Get input for training stage\n\n    :param filenames: A list contains [source_filename, target_filename]\n    :param params: Hyper-parameters\n\n    :returns: A dictionary of pair <Key, Tensor>\n    '
    with tf.device('/cpu:0'):
        src_dataset = tf.data.TextLineDataset(filenames[0])
        tgt_dataset = tf.data.TextLineDataset(filenames[1])
        dataset = tf.data.Dataset.zip((src_dataset, tgt_dataset))
        dataset = dataset.shuffle(params.buffer_size)
        dataset = dataset.repeat()
        dataset = dataset.map((lambda src, tgt: (tf.string_split([src]).values, tf.string_split([tgt]).values)), num_parallel_calls=params.num_threads)
        dataset = dataset.map((lambda src, tgt: (tf.concat([src, [tf.constant(params.eos)]], axis=0), tf.concat([tgt, [tf.constant(params.eos)]], axis=0))), num_parallel_calls=params.num_threads)
        dataset = dataset.map((lambda src, tgt: {'source': src, 'target': tgt, 'source_length': tf.shape(src), 'target_length': tf.shape(tgt)}), num_parallel_calls=params.num_threads)
        iterator = dataset.make_one_shot_iterator()
        features = iterator.get_next()
        src_table = tf.contrib.lookup.index_table_from_tensor(tf.constant(params.vocabulary['source']), default_value=params.mapping['source'][params.unk])
        tgt_table = tf.contrib.lookup.index_table_from_tensor(tf.constant(params.vocabulary['target']), default_value=params.mapping['target'][params.unk])
        features['source'] = src_table.lookup(features['source'])
        features['target'] = tgt_table.lookup(features['target'])
        shard_multiplier = (len(params.device_list) * params.update_cycle)
        features = batch_examples(features, params.batch_size, params.max_length, params.mantissa_bits, shard_multiplier=shard_multiplier, length_multiplier=params.length_multiplier, constant=params.constant_batch_size, num_threads=params.num_threads)
        features['source'] = tf.to_int32(features['source'])
        features['target'] = tf.to_int32(features['target'])
        features['source_length'] = tf.to_int32(features['source_length'])
        features['target_length'] = tf.to_int32(features['target_length'])
        features['source_length'] = tf.squeeze(features['source_length'], 1)
        features['target_length'] = tf.squeeze(features['target_length'], 1)
        return features

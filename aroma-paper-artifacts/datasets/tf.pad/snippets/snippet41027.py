import tensorflow as tf
import numpy as np
from collections import namedtuple
from abc import abstractmethod
from utils.tfrecord import parse_preprocessed_mel_data, decode_preprocessed_mel_data, PreprocessedMelData


def padding_function(t):
    tail_padding = (padded_target_length - target_length)
    padding_shape = tf.sparse_tensor_to_dense(tf.SparseTensor(indices=[(0, 1)], values=tf.expand_dims(tail_padding, axis=0), dense_shape=(2, 2)))
    return (lambda : tf.pad(t, paddings=padding_shape, constant_values=hparams.silence_mel_level_db))

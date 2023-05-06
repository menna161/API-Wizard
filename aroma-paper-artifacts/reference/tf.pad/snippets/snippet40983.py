import tensorflow as tf
import numpy as np
from collections import namedtuple
from abc import abstractmethod
from utils.tfrecord import parse_preprocessed_mel_data, decode_preprocessed_mel_data, PreprocessedMelData


def convert(target: PreprocessedMelData):
    r = hparams.outputs_per_step
    mel_normalized = ((target.mel - np.array(hparams.average_mel_level_db, dtype=np.float32)) / np.array(hparams.stddev_mel_level_db, dtype=np.float32))
    mel_with_silence = tf.pad(mel_normalized, paddings=[[r, r], [0, 0]], constant_values=hparams.silence_mel_level_db)
    target_length = (target.target_length + (2 * r))
    padded_target_length = (((target_length // r) + 1) * r)

    def padding_function(t):
        tail_padding = (padded_target_length - target_length)
        padding_shape = tf.sparse_tensor_to_dense(tf.SparseTensor(indices=[(0, 1)], values=tf.expand_dims(tail_padding, axis=0), dense_shape=(2, 2)))
        return (lambda : tf.pad(t, paddings=padding_shape, constant_values=hparams.silence_mel_level_db))
    no_padding_condition = tf.equal(tf.to_int64(0), (target_length % r))
    mel = tf.cond(no_padding_condition, (lambda : mel_with_silence), padding_function(mel_with_silence))
    mel.set_shape((None, hparams.num_mels))
    padded_target_length = tf.cond(no_padding_condition, (lambda : target_length), (lambda : padded_target_length))
    done = tf.concat([tf.zeros(((padded_target_length // r) - 1), dtype=tf.float32), tf.ones(1, dtype=tf.float32)], axis=0)
    spec_loss_mask = tf.ones(shape=padded_target_length, dtype=tf.float32)
    binary_loss_mask = tf.ones(shape=(padded_target_length // r), dtype=tf.float32)
    return MelData(target.id, target.key, mel, target.mel_width, padded_target_length, done, spec_loss_mask, binary_loss_mask)

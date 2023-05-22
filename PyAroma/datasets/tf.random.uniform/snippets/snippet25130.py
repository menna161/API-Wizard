import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def perceptual_loss(features, max_pairs=1000, MULTIPLIER=(- 1)):
    'Return a negative value, where greater magnitudes describe further distances.\n  This is to encourage samples to be perceptually more distant from each other.\n  i.e., they are repelled from each other.\n  '
    b_s = features.shape[0]
    num_pairs = ((b_s * (b_s - 1)) // 2)
    pair_idxs = tf.where(tf.ones((b_s, b_s)))
    non_matching_pairs = tf.squeeze(tf.where((pair_idxs[(:, 0)] < pair_idxs[(:, 1)])))
    pair_idxs = tf.gather(pair_idxs, non_matching_pairs)
    num_pairs = min([num_pairs, max_pairs])
    use_pair_idxs = tf.random.uniform([num_pairs], minval=0, maxval=num_pairs, dtype=tf.int32)
    pair_idxs = tf.gather(pair_idxs, use_pair_idxs)
    features = tf.math.reduce_mean(features, [1, 2])
    feature_pairs = tf.gather(features, pair_idxs)
    diffs = (feature_pairs[(:, 0)] - feature_pairs[(:, 1)])
    diffs = tf.math.reduce_mean(tf.abs(diffs), axis=(- 1))
    percept_loss = tf.math.reduce_mean(diffs)
    percept_loss = tf.sqrt(percept_loss)
    percept_loss = (percept_loss * MULTIPLIER)
    return percept_loss

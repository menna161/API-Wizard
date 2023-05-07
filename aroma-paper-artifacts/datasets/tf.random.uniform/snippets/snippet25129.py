import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def vector_distance_loss(rep1, rep2, max_pairs=1000):
    "Experimental loss score based on trying to match the distance between\n  corresponding pairs of representations, using logistic loss between distances\n  normalized from 0 to 1. No idea how stable this will be!\n\n  This use case: match the distances between pairs of images perceptions with\n  the distances between pairs of symbol labels.\n\n  Update: this is likely not necessary because graph pretraining actually hasn't\n  shown to provide a major qualitative improvement, so there is nothing\n  particularly special about the graph embeddings vs. visual latent spaces.\n  Still curious!\n  "
    n = rep1.shape[0]
    assert (n >= 4)
    num_pairs = ((rep1.shape[0] * (rep1.shape[0] - 1)) // 2)
    pairs = tf.where(tf.ones((n, n)))
    unique_pairs = tf.squeeze(tf.where((pairs[(:, 0)] < pairs[(:, 1)])))
    pairs = tf.gather(pairs, unique_pairs)
    num_pairs = min([num_pairs, max_pairs])
    use_pair_idxs = tf.random.uniform([num_pairs], minval=0, maxval=num_pairs, dtype=tf.int32)
    pairs = tf.gather(pairs, use_pair_idxs)
    pairs1 = tf.gather(rep1, pairs)
    diffs1 = tf.abs((pairs1[(:, 0)] - pairs1[(:, 1)]))
    diffs1 = tf.math.reduce_mean(diffs1, axis=(tf.range((tf.rank(diffs1) - 1)) + 1))
    pairs2 = tf.gather(rep2, pairs)
    diffs2 = tf.abs((pairs2[(:, 0)] - pairs2[(:, 1)]))
    diffs2 = tf.math.reduce_mean(diffs2, axis=(tf.range((tf.rank(diffs2) - 1)) + 1))

    def zero_one_normalize(tensor):
        tensor = (tensor / tf.math.reduce_max(tensor))
        return tensor
    diffs1 = zero_one_normalize(diffs1)
    diffs2 = zero_one_normalize(diffs2)
    diffs1 = diffs1[(:, tf.newaxis)]
    diffs2 = diffs2[(:, tf.newaxis)]
    error = tf.keras.losses.binary_crossentropy(diffs1, diffs2)
    error = tf.math.reduce_mean(error)
    return error

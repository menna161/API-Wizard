import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def make_symbol_data(num_samples, NUM_SYMBOLS, test=False, **kwargs):
    'Generate training data for toy problem (no GraphVAE)\n  '
    _num_samples = (int((num_samples * 0.2)) if test else num_samples)
    x = tf.random.uniform((_num_samples,), 0, NUM_SYMBOLS, dtype=tf.int32)
    x = tf.one_hot(x, depth=NUM_SYMBOLS)
    samples = tf.range(NUM_SYMBOLS)
    samples = tf.one_hot(samples, depth=NUM_SYMBOLS)
    return (x, samples)

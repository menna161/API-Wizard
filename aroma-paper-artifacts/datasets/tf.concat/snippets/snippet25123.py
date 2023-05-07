import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def generate_scaled_coordinate_hints(batch_size, y_dim, x_dim):
    'Generally used as the input to a CPPN, but can also augment each layer\n  of a ConvNet with location hints\n  '
    spatial_scale = (1.0 / max([y_dim, x_dim]))
    coord_ints = get_coord_ints(y_dim, x_dim)
    coords = tf.cast(coord_ints, tf.float32)
    coords = tf.stack([(coords[(:, :, 0)] * spatial_scale), (coords[(:, :, 1)] * spatial_scale)], axis=(- 1))
    dists = tf.stack([(coords[(:, :, 0)] - 0.5), (coords[(:, :, 1)] - 0.5)], axis=(- 1))
    r = tf.sqrt(tf.math.reduce_sum((dists ** 2), axis=(- 1)))[(..., tf.newaxis)]
    loc = tf.concat([coords, r], axis=(- 1))
    loc = tf.tile(loc[tf.newaxis], [batch_size, 1, 1, 1])
    return loc

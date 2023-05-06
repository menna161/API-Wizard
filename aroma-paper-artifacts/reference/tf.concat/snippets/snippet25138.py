import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def call(self, Z):
    batch_size = Z.shape[0]
    coord_ints = get_coord_ints(self.y_dim, self.x_dim)
    coords = tf.cast(coord_ints, tf.float32)
    coords = tf.stack([(coords[(:, :, 0)] * self.spatial_scale), (coords[(:, :, 1)] * self.spatial_scale)], axis=(- 1))
    dists = tf.stack([(coords[(:, :, 0)] - 0.5), (coords[(:, :, 1)] - 0.5)], axis=(- 1))
    r = tf.sqrt(tf.math.reduce_sum((dists ** 2), axis=(- 1)))[(..., tf.newaxis)]
    loc = tf.concat([coords, r], axis=(- 1))
    loc = self.loc_embed(loc)
    loc = tf.tile(loc[tf.newaxis], [batch_size, 1, 1, 1])
    Z = self.Z_embed(Z)
    Z = tf.tile(Z[(:, tf.newaxis, tf.newaxis)], [1, self.y_dim, self.x_dim, 1])
    x = tf.concat([loc, Z], axis=(- 1))
    x = self.in_w(x)
    for layer in self.ws:
        start_x = x
        x = layer(x)
        x = (x + start_x)
        x = tf.nn.swish(x)
    x = self.out_w(x)
    x = tf.nn.tanh(x)
    if (x.shape[(- 1)] == 1):
        x = tf.tile(x, [1, 1, 1, 3])
    return x

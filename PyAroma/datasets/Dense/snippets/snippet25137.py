import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def __init__(self, y_dim: int, x_dim: int, vision_hidden_size: int, R: int, cppn_loc_embed_dim, cppn_Z_embed_dim: int, c_out: int=1, **kwargs):
    super(CPPN, self).__init__()
    self.loc_embed = tf.keras.layers.Dense(cppn_loc_embed_dim, **dense_regularization)
    self.Z_embed = tf.keras.layers.Dense(cppn_Z_embed_dim, **dense_regularization)
    self.in_w = tf.keras.layers.Dense(vision_hidden_size, **dense_regularization)
    self.ws = [tf.keras.layers.Dense(vision_hidden_size, **dense_regularization) for _ in range(R)]
    self.out_w = tf.keras.layers.Dense(c_out, **dense_regularization)
    self.y_dim = y_dim
    self.x_dim = x_dim
    self.spatial_scale = (1 / max([y_dim, x_dim]))
    self.output_scale = (1.0 / tf.math.sqrt(tf.cast(vision_hidden_size, tf.float32)))

import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def __init__(self, y_dim: int, x_dim: int, vision_hidden_size: int, R: int, c_out: int, NUM_SYMBOLS: int, minimum_filters: int, **kwargs):
    super(ConvDiscriminator, self).__init__()
    self.res_preps = []
    self.residual_blocks_1 = []
    self.residual_blocks_2 = []
    self.maxpools = []
    for r in range(R):
        filters = (vision_hidden_size // (2 ** ((R - r) - 1)))
        filters = max([filters, minimum_filters])
        res_prep = tf.keras.layers.Conv2D(filters, kernel_size=1, strides=1, padding='same', **cnn_regularization)
        residual_block_1 = ResidualBlock(filters)
        residual_block_2 = ResidualBlock(filters)
        self.res_preps.append(res_prep)
        self.residual_blocks_1.append(residual_block_1)
        self.residual_blocks_2.append(residual_block_2)
        self.maxpools.append(tf.keras.layers.Conv2D(filters, kernel_size=3, strides=2, padding='same', **cnn_regularization))
    self.out_conv = tf.keras.layers.Conv2D(vision_hidden_size, kernel_size=1, strides=1, padding='same', **dense_regularization)
    self.pred = tf.keras.layers.Dense(NUM_SYMBOLS, **dense_regularization)
    self.gap = tf.keras.layers.GlobalAveragePooling2D()

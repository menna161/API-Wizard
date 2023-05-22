import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization, cnn_regularization
from ccn.cfg import get_config


def __init__(self, y_dim: int, x_dim: int, vision_hidden_size: int, R: int, c_out: int, Z_embed_num: int, minimum_filters: int, **kwargs):
    super(ConvGenerator, self).__init__()
    self.init_Z_embed = tf.keras.layers.Dense(vision_hidden_size, **dense_regularization)
    self.y_dim = y_dim
    self.x_dim = x_dim
    self.res_preps = []
    self.residual_blocks_1 = []
    self.residual_blocks_2 = []
    self.upsamples = []
    self.Z_embeds = []
    self.Z_norms = []
    self.cond_convs = []
    for r in range(R):
        filters = (vision_hidden_size // (2 ** (R - r)))
        filters = max([filters, minimum_filters])
        Z_filters = (filters // 4)
        res_prep = tf.keras.layers.Conv2D(filters, kernel_size=1, strides=1, padding='same', **cnn_regularization)
        residual_block_1 = ResidualBlock(filters)
        residual_block_2 = ResidualBlock(filters)
        upsample = tf.keras.layers.Conv2DTranspose(filters, kernel_size=3, strides=2, padding='same', **cnn_regularization)
        Z_embeds = ([tf.keras.layers.Dense(256, **dense_regularization) for _ in range((Z_embed_num - 1))] + [tf.keras.layers.Dense(Z_filters, **dense_regularization)])
        Z_norms = [tf.keras.layers.BatchNormalization() for _ in range(Z_embed_num)]
        cond_conv = tf.keras.layers.Conv2D(filters, kernel_size=1, strides=1, padding='same')
        self.res_preps = ([res_prep] + self.res_preps)
        self.residual_blocks_1 = ([residual_block_1] + self.residual_blocks_1)
        self.residual_blocks_2 = ([residual_block_2] + self.residual_blocks_2)
        self.upsamples = ([upsample] + self.upsamples)
        self.Z_embeds = ([Z_embeds] + self.Z_embeds)
        self.Z_norms = ([Z_norms] + self.Z_norms)
        self.cond_convs = ([cond_conv] + self.cond_convs)
    self.out_conv = tf.keras.layers.Conv2D(c_out, kernel_size=1, strides=1, padding='same', **cnn_regularization)

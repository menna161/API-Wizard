from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def __init__(self, num_heads: int, graph_hidden_size: int):
    super(GlobalAttention, self).__init__()
    self.num_heads = num_heads
    self.graph_hidden_size = graph_hidden_size
    self.scale = (1.0 / tf.math.sqrt(tf.cast(graph_hidden_size, tf.float32)))
    self.q_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.k_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.v_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.w_out_1 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_1 = tf.keras.layers.LayerNormalization()
    self.w_out_2 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_2 = tf.keras.layers.LayerNormalization()
    self.w_out_3 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_3 = tf.keras.layers.LayerNormalization()

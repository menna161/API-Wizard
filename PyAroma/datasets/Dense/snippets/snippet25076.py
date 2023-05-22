from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def __init__(self, num_heads: int, graph_hidden_size: int, max_nodes: int):
    'Multi-head global self-attention (based generally on the original\n    Transformer paper) combined with local graph attention (Graph Attention\n    Networks.)\n\n    Attention Is All You Need by Vaswani et al.\n    https://arxiv.org/abs/1706.03762\n\n    Graph Attention Networks by Veličković et al.\n    https://arxiv.org/abs/1710.10903\n\n    This layer incorporates a multi-head self-attention module as well as\n    a feed-forward layer with the swish activation function.\n    '
    super(GlobalLocalAttention, self).__init__()
    self.max_nodes = max_nodes
    self.num_heads = num_heads
    self.graph_hidden_size = graph_hidden_size
    self.scale = (1.0 / tf.math.sqrt(tf.cast(graph_hidden_size, tf.float32)))
    self.local_q_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.local_k_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.local_v_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.global_q_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.global_k_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.global_v_ws = [tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for _ in range(num_heads)]
    self.w_out_1 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_1 = tf.keras.layers.LayerNormalization()
    self.w_out_2 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_2 = tf.keras.layers.LayerNormalization()
    self.w_out_3 = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_3 = tf.keras.layers.LayerNormalization()

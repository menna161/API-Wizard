from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def __init__(self, num_heads: int, graph_hidden_size: int, max_nodes: int, node_feature_specs: Dict[(str, int)], decoder_attention_layers: int, **kwargs):
    "Simple graph reconstruction with dense feed-forward neural network based\n    generally on the GraphVAE paper. Added global self-attention as a refining\n    step which improves accuracy.\n\n    ---\n    GraphVAE: Towards Generation of Small Graphs Using Variational Autoencoders,\n    Simonovsky et al.\n    https://arxiv.org/abs/1802.03480\n    ---\n\n    Args:\n      num_heads\n      hidden_size\n      max_nodes\n      node_feature_specs: a dict of integers, each mapping a node feature name\n        to its dimensionality. Example: {'ord': 4}\n    "
    super(GraphDecoder, self).__init__()
    self._name = 'g_decoder'
    self.max_nodes = max_nodes
    self.expand_w = tf.keras.layers.Dense((max_nodes * graph_hidden_size), **dense_regularization)
    self.pos_embeds = [tf.keras.layers.Dense(128, **dense_regularization) for _ in range(3)]
    self.pos_norms = [tf.keras.layers.LayerNormalization() for _ in range(3)]
    self.combine_pos = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.combine_pos_norm = tf.keras.layers.LayerNormalization()
    self.global_attns = [GlobalAttention(num_heads, graph_hidden_size) for _ in range(decoder_attention_layers)]
    self.adj_w = tf.keras.layers.Dense(max_nodes, name='adjacency', **dense_regularization)
    self.nf_w = {name: tf.keras.layers.Dense((size + 1), name=f'feature_{name}', **dense_regularization) for (name, size) in node_feature_specs.items()}
    self.scale = (1.0 / tf.math.sqrt(tf.cast(graph_hidden_size, tf.float32)))
    self.graph_hidden_size = graph_hidden_size

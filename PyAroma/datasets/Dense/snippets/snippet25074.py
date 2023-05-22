from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def __init__(self, graph_hidden_size: int, node_feature_specs: Dict[(str, int)]):
    super(NodeFeatureEmbed, self).__init__()
    self.nf_w = {name: tf.keras.layers.Dense(graph_hidden_size, **dense_regularization) for name in node_feature_specs.keys()}
    self.w = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_1 = tf.keras.layers.LayerNormalization()
    self.w_out = tf.keras.layers.Dense(graph_hidden_size, **dense_regularization)
    self.layer_norm_2 = tf.keras.layers.LayerNormalization()

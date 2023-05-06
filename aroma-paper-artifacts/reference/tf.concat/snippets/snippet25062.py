import os
import random
import code
from typing import Dict
import tensorflow as tf
import numpy as np
from graphviz import Digraph
from tqdm import tqdm


def label_data(node_features, adj, num_nodes):
    nf_labels = {}
    for name in node_features.keys():
        empty_rows = (tf.math.reduce_max(node_features[name], axis=(- 1)) == 0)[(:, :, tf.newaxis)]
        empty_rows = tf.cast(empty_rows, tf.float32)
        nf_labels[name] = tf.concat([node_features[name], empty_rows], axis=(- 1))
    identity = tf.eye(adj.shape[1], adj.shape[1], batch_shape=[adj.shape[0]], dtype=tf.int32)
    r = tf.range(adj.shape[1])
    grid_max_idxs = tf.tile(tf.expand_dims(tf.math.maximum(r[tf.newaxis], r[(:, tf.newaxis)]), 0), [num_nodes.shape[0], 1, 1])
    identity = tf.where((grid_max_idxs < num_nodes[(:, tf.newaxis, tf.newaxis)]), identity, tf.zeros_like(identity))
    adj_labels = (adj + identity)
    return (nf_labels, adj_labels)

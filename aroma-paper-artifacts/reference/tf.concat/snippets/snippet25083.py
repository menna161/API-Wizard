from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def call(self, Z, debug=False):
    '\n    Inputs:\n      Z: tensor of shape [batch_size, node_embedding], which is a\n    fixed-dimensional representation of a graph that will be reconstructed to\n    its nodes.\n    '
    batch_size = Z.shape[0]
    expanded_x = self.expand_w(Z)
    expanded_x = tf.nn.swish(expanded_x)
    x = tf.reshape(expanded_x, [batch_size, self.max_nodes, self.graph_hidden_size])
    pos = tf.tile(tf.range(self.max_nodes)[tf.newaxis], [x.shape[0], 1])
    pos = (tf.cast(pos, tf.float32)[(..., tf.newaxis)] / self.max_nodes)
    for (pos_embed, pos_norm) in zip(self.pos_embeds, self.pos_norms):
        pos = pos_embed(pos)
        pos = pos_norm(pos)
    x = tf.concat([pos, x], axis=(- 1))
    x = self.combine_pos(x)
    x = self.combine_pos_norm(x)
    for attn_layer in self.global_attns:
        x = attn_layer(x)
    adj_out = self.adj_w(x)
    adj_out = (self.scale * adj_out)
    adj_out = tf.nn.sigmoid(adj_out)
    nf_out = {}
    for name in self.nf_w.keys():
        w_layer = self.nf_w[name]
        nf_pred = w_layer(x)
        nf_pred = (self.scale * nf_pred)
        nf_pred = tf.nn.softmax(nf_pred)
        nf_out[name] = nf_pred
    return (adj_out, nf_out)

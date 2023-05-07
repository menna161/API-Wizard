from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def call(self, inputs):
    '\n    Inputs:\n      x: tensor of shape [batch_size, max_nodes, node_embedding]\n      num_nodes: a tensor of shape [batch_size] stating the number of nodes per\n        input graph\n    '
    x = inputs['x']
    start_x = tf.nn.dropout(x, 0.1)
    num_nodes = inputs['num_nodes']
    adj = inputs['adj']
    Qs = [q_w(x) for q_w in self.global_q_ws]
    Ks = [k_w(x) for k_w in self.global_k_ws]
    Vs = [v_w(x) for v_w in self.global_v_ws]
    Es = [tf.matmul(q, k, transpose_b=True) for (q, k) in zip(Qs, Ks)]
    Es = [(self.scale * e) for e in Es]
    mask = tf.sequence_mask(num_nodes, maxlen=self.max_nodes)[(:, tf.newaxis)]
    r = tf.range(self.max_nodes)
    grid_max_idxs = tf.tile(tf.expand_dims(tf.math.maximum(r[tf.newaxis], r[(:, tf.newaxis)]), 0), [num_nodes.shape[0], 1, 1])
    mask = (grid_max_idxs < num_nodes[(:, tf.newaxis, tf.newaxis)])
    Es = [tf.where(mask, e, (tf.ones_like(e) * (- 1000000000.0))) for e in Es]
    scores = [tf.nn.softmax(e) for e in Es]
    global_context = [tf.matmul(score, v) for (score, v) in zip(scores, Vs)]
    global_context = tf.concat(global_context, axis=(- 1))
    Qs = [q_w(x) for q_w in self.local_q_ws]
    Ks = [k_w(x) for k_w in self.local_k_ws]
    Vs = [v_w(x) for v_w in self.local_v_ws]
    Es = [tf.matmul(q, k, transpose_b=True) for (q, k) in zip(Qs, Ks)]
    Es = [(self.scale * e) for e in Es]
    adj = (adj + tf.eye(adj.shape[1], adj.shape[1], batch_shape=[adj.shape[0]], dtype=tf.int32))
    Es = [tf.where((adj == 1), e, (tf.ones_like(e) * (- 1000000000.0))) for e in Es]
    scores = [tf.nn.softmax(e) for e in Es]
    local_context = [tf.matmul(score, v) for (score, v) in zip(scores, Vs)]
    local_context = tf.concat(local_context, axis=(- 1))
    context = tf.concat([global_context, local_context], axis=(- 1))
    x = self.w_out_1(context)
    x = self.layer_norm_1(x)
    x = (start_x + x)
    x = tf.nn.swish(x)
    res_x = x
    x = self.w_out_2(x)
    x = self.layer_norm_2(x)
    x = (res_x + x)
    x = tf.nn.swish(x)
    res_x = x
    x = self.w_out_3(x)
    x = self.layer_norm_3(x)
    x = (res_x + x)
    x = tf.nn.swish(x)
    return x

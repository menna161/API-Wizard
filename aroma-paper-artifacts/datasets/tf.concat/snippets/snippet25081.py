from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def call(self, x):
    start_x = tf.nn.dropout(x, 0.1)
    Qs = [q_w(x) for q_w in self.q_ws]
    Ks = [k_w(x) for k_w in self.k_ws]
    Vs = [v_w(x) for v_w in self.v_ws]
    Es = [tf.matmul(q, k, transpose_b=True) for (q, k) in zip(Qs, Ks)]
    Es = [(self.scale * e) for e in Es]
    scores = [tf.nn.softmax(e) for e in Es]
    context = [tf.matmul(score, v) for (score, v) in zip(scores, Vs)]
    context = tf.concat(context, axis=(- 1))
    x = self.w_out_1(context)
    x = self.layer_norm_1(x)
    x = (start_x + x)
    x = tf.nn.swish(x)
    res_x = x
    res_x_2 = x
    x = self.w_out_2(x)
    x = self.layer_norm_2(x)
    x = (res_x + x)
    x = tf.nn.swish(x)
    res_x = x
    x = self.w_out_3(x)
    x = self.layer_norm_3(x)
    x = ((res_x_2 + res_x) + x)
    x = tf.nn.swish(x)
    return x

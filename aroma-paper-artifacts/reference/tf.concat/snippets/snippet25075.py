from typing import Dict
import code
import tensorflow as tf
import tensorflow_addons as tfa
from ccn.ml_utils import dense_regularization


def call(self, inputs):
    nf = inputs['node_features']
    feature_reps = []
    for (name, layer) in self.nf_w.items():
        nf_rep = layer(nf[name])
        nf_rep = tf.nn.swish(nf_rep)
        feature_reps.append(nf_rep)
    feature_reps = tf.concat(feature_reps, axis=(- 1))
    x = self.w(feature_reps)
    x = self.layer_norm_1(x)
    pre_linear_x = x
    x = tf.nn.swish(x)
    x = self.w_out(x)
    x = self.layer_norm_2(x)
    x = (pre_linear_x + x)
    x = tf.nn.swish(x)
    return x

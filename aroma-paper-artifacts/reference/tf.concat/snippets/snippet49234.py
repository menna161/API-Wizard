import numpy as np
import tensorflow as tf
from tensorflow.contrib.training import HParams


def attn(x, scope, n_state, *, past, hparams):
    assert (x.shape.ndims == 3)
    assert ((n_state % hparams.n_head) == 0)
    if (past is not None):
        assert (past.shape.ndims == 5)

    def split_heads(x):
        return tf.transpose(split_states(x, hparams.n_head), [0, 2, 1, 3])

    def merge_heads(x):
        return merge_states(tf.transpose(x, [0, 2, 1, 3]))

    def mask_attn_weights(w):
        (_, _, nd, ns) = shape_list(w)
        b = attention_mask(nd, ns, dtype=w.dtype)
        b = tf.reshape(b, [1, 1, nd, ns])
        w = ((w * b) - (tf.cast(10000000000.0, w.dtype) * (1 - b)))
        return w

    def multihead_attn(q, k, v):
        w = tf.matmul(q, k, transpose_b=True)
        w = (w * tf.rsqrt(tf.cast(v.shape[(- 1)].value, w.dtype)))
        w = mask_attn_weights(w)
        w = softmax(w)
        a = tf.matmul(w, v)
        return a
    with tf.variable_scope(scope):
        c = conv1d(x, 'c_attn', (n_state * 3))
        (q, k, v) = map(split_heads, tf.split(c, 3, axis=2))
        present = tf.stack([k, v], axis=1)
        if (past is not None):
            (pk, pv) = tf.unstack(past, axis=1)
            k = tf.concat([pk, k], axis=(- 2))
            v = tf.concat([pv, v], axis=(- 2))
        a = multihead_attn(q, k, v)
        a = merge_heads(a)
        a = conv1d(a, 'c_proj', n_state)
        return (a, present)

import keras
import keras.backend as K
import tensorflow as tf
from matchzoo.engine.base_model import BaseModel
from matchzoo.engine.param import Param
from matchzoo.engine import hyper_spaces


def attention(tensors):
    'Attention layer.'
    (left, right) = tensors
    tensor_left = tf.expand_dims(left, axis=2)
    tensor_right = tf.expand_dims(right, axis=1)
    tensor_left = K.repeat_elements(tensor_left, len_right, 2)
    tensor_right = K.repeat_elements(tensor_right, len_left, 1)
    tensor_merged = tf.concat([tensor_left, tensor_right], axis=(- 1))
    middle_output = keras.layers.Dense(self._params['fc_num_units'], activation='tanh')(tensor_merged)
    attn_scores = keras.layers.Dense(1)(middle_output)
    attn_scores = tf.squeeze(attn_scores, axis=3)
    exp_attn_scores = tf.math.exp((attn_scores - tf.reduce_max(attn_scores, axis=(- 1), keepdims=True)))
    exp_sum = tf.reduce_sum(exp_attn_scores, axis=(- 1), keepdims=True)
    attention_weights = (exp_attn_scores / exp_sum)
    return K.batch_dot(attention_weights, right)

import keras
import keras.backend as K
import tensorflow as tf
from matchzoo.engine.base_model import BaseModel
from matchzoo.engine.param import Param
from matchzoo.engine import hyper_spaces


def build(self):
    'Build model.'
    (input_left, input_right) = self._make_inputs()
    len_left = input_left.shape[1]
    len_right = input_right.shape[1]
    embedding = self._make_embedding_layer()
    embed_left = embedding(input_left)
    embed_right = embedding(input_right)
    lstm_left = keras.layers.LSTM(self._params['lstm_num_units'], return_sequences=True, name='lstm_left')
    lstm_right = keras.layers.LSTM(self._params['lstm_num_units'], return_sequences=True, name='lstm_right')
    encoded_left = lstm_left(embed_left)
    encoded_right = lstm_right(embed_right)

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
    attn_layer = keras.layers.Lambda(attention)
    left_attn_vec = attn_layer([encoded_left, encoded_right])
    concat = keras.layers.Concatenate(axis=1)([left_attn_vec, encoded_right])
    lstm_merge = keras.layers.LSTM((self._params['lstm_num_units'] * 2), return_sequences=False, name='lstm_merge')
    merged = lstm_merge(concat)
    dropout = keras.layers.Dropout(rate=self._params['dropout_rate'])(merged)
    phi = keras.layers.Dense(self._params['fc_num_units'], activation='tanh')(dropout)
    inputs = [input_left, input_right]
    out = self._make_output_layer()(phi)
    self._backend = keras.Model(inputs=inputs, outputs=[out])

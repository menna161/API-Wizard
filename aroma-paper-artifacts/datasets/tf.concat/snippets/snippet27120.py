import tensorflow as tf
from keras import backend as K
from keras.engine import Layer
from matchzoo.contrib.layers.attention_layer import AttentionLayer


def call(self, x: list, **kwargs):
    'Call.'
    (seq_lt, seq_rt) = (x[:5], x[5:])
    (lstm_reps_lt, forward_h_lt, _, backward_h_lt, _) = seq_lt
    (lstm_reps_rt, forward_h_rt, _, backward_h_rt, _) = seq_rt
    match_tensor_list = []
    match_dim = 0
    if self._perspective.get('full'):
        h_lt = tf.concat([forward_h_lt, backward_h_lt], axis=(- 1))
        full_match_tensor = self.full_match([h_lt, lstm_reps_rt])
        match_tensor_list.append(full_match_tensor)
        match_dim += (self._mp_dim + 1)
    if self._perspective.get('max-pooling'):
        max_match_tensor = self.max_pooling_match([lstm_reps_lt, lstm_reps_rt])
        match_tensor_list.append(max_match_tensor)
        match_dim += self._mp_dim
    if self._perspective.get('attentive'):
        attentive_tensor = self.attentive_match([lstm_reps_lt, lstm_reps_rt])
        match_tensor_list.append(attentive_tensor)
        match_dim += (self._mp_dim + 1)
    if self._perspective.get('max-attentive'):
        relevancy_matrix = _calc_relevancy_matrix(lstm_reps_lt, lstm_reps_rt)
        max_attentive_tensor = self.max_attentive_match([lstm_reps_lt, lstm_reps_rt, relevancy_matrix])
        match_tensor_list.append(max_attentive_tensor)
        match_dim += (self._mp_dim + 1)
    mp_tensor = tf.concat(match_tensor_list, axis=(- 1))
    return mp_tensor

import tensorflow as tf
from keras import backend as K
from keras.engine import Layer
from matchzoo.contrib.layers.attention_layer import AttentionLayer


def _multi_perspective_match(mp_dim, reps_rt, att_lt, with_cosine=True, with_mp_cosine=True):
    "\n    The core function of zhiguowang's implementation.\n\n    reference:\n    https://github.com/zhiguowang/BiMPM/blob/master/src/match_utils.py#L207-L223\n    :param mp_dim: about 20\n    :param reps_rt: [batch, len_rt, dim]\n    :param att_lt: [batch, len_rt, dim]\n    :param with_cosine: True\n    :param with_mp_cosine: True\n    :return: [batch, len, 1 + mp_dim]\n    "
    shape_rt = tf.shape(reps_rt)
    batch_size = shape_rt[0]
    len_lt = shape_rt[1]
    match_dim = 0
    match_result_list = []
    if with_cosine:
        cosine_tensor = _cosine_distance(reps_rt, att_lt, False)
        cosine_tensor = tf.reshape(cosine_tensor, [batch_size, len_lt, 1])
        match_result_list.append(cosine_tensor)
        match_dim += 1
    if with_mp_cosine:
        mp_cosine_layer = MpCosineLayer(mp_dim)
        mp_cosine_tensor = mp_cosine_layer([reps_rt, att_lt])
        mp_cosine_tensor = tf.reshape(mp_cosine_tensor, [batch_size, len_lt, mp_dim])
        match_result_list.append(mp_cosine_tensor)
        match_dim += mp_cosine_layer.mp_dim
    match_result = tf.concat(match_result_list, 2)
    return (match_result, match_dim)

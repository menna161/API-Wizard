import numpy as np
import tensorflow as tf
import keras.backend as K
import keras.layers as L
from keras.models import Model
from .zerogru import ZeroGRU, NestedTimeDist


def build_model(char_size=27, dim=64, iterations=4, training=True, pca=False):
    'Build the model.'
    context = L.Input(shape=(None, None, None), name='context', dtype='int32')
    query = L.Input(shape=(None,), name='query', dtype='int32')
    var_flat = L.Lambda((lambda x: K.reshape(x, K.stack([K.shape(x)[0], (- 1), K.prod(K.shape(x)[2:])]))), name='var_flat')
    flat_ctx = var_flat(context)
    onehot_weights = np.eye(char_size)
    onehot_weights[(0, 0)] = 0
    onehot = L.Embedding(char_size, char_size, trainable=False, weights=[onehot_weights], name='onehot')
    embedded_ctx = onehot(flat_ctx)
    embedded_q = onehot(query)
    embed_pred = ZeroGRU(dim, go_backwards=True, name='embed_pred')
    embedded_predq = embed_pred(embedded_q)
    embedded_rules = NestedTimeDist(embed_pred, name='rule_embed')(embedded_ctx)
    repeat_toctx = L.RepeatVector(K.shape(embedded_ctx)[1], name='repeat_to_ctx')
    diff_sq = L.Lambda((lambda xy: K.square((xy[0] - xy[1]))), output_shape=(None, dim), name='diff_sq')
    concat = L.Lambda((lambda xs: K.concatenate(xs, axis=2)), output_shape=(None, (dim * 5)), name='concat')
    att_dense1 = L.TimeDistributed(L.Dense(dim, activation='tanh', name='att_dense1'), name='d_att_dense1')
    att_dense2 = L.TimeDistributed(L.Dense(1, activation='sigmoid', name='att_dense2'), name='d_att_dense2')
    squeeze2 = L.Lambda((lambda x: K.squeeze(x, 2)), name='sequeeze2')
    rule_mask = L.Lambda((lambda x: K.cast(K.any(K.not_equal(x, 0), axis=(- 1), keepdims=True), 'float32')), name='rule_mask')(embedded_rules)
    episodic_mem = EpisodicMemory(dim, name='episodic_mem')
    state = embedded_predq
    repeated_q = repeat_toctx(embedded_predq)
    outs = list()
    for _ in range(iterations):
        ctx_state = repeat_toctx(state)
        s_s_c = diff_sq([ctx_state, embedded_rules])
        s_m_c = L.multiply([embedded_rules, state])
        sim_vec = concat([s_s_c, s_m_c, ctx_state, embedded_rules, repeated_q])
        sim_vec = att_dense1(sim_vec)
        sim_vec = att_dense2(sim_vec)
        sim_vec = L.multiply([sim_vec, rule_mask])
        state = episodic_mem([state, sim_vec, embedded_rules])
        sim_vec = squeeze2(sim_vec)
        outs.append(sim_vec)
    out = L.Dense(1, activation='sigmoid', name='out')(state)
    if pca:
        model = Model([context, query], [embedded_rules])
    elif training:
        model = Model([context, query], [out])
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    else:
        model = Model([context, query], (outs + [out]))
    return model

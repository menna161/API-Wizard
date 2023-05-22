import numpy as np
import keras.backend as K
import keras.layers as L
from keras.models import Model
from .zerogru import ZeroGRU, NestedTimeDist


def build_model(char_size=27, dim=64, iterations=4, training=True, ilp=False, pca=False):
    'Build the model.'
    context = L.Input(shape=(None, None, None), name='context', dtype='int32')
    query = L.Input(shape=(None,), name='query', dtype='int32')
    if ilp:
        (context, query, templates) = ilp
    onehot_weights = np.eye(char_size)
    onehot_weights[(0, 0)] = 0
    onehot = L.Embedding(char_size, char_size, trainable=False, weights=[onehot_weights], name='onehot')
    embedded_ctx = onehot(context)
    embedded_q = onehot(query)
    if ilp:
        embedded_ctx = L.Lambda((lambda xs: K.concatenate(xs, axis=1)), name='template_concat')([templates, embedded_ctx])
    embed_pred = ZeroGRU(dim, go_backwards=True, name='embed_pred')
    embedded_predq = embed_pred(embedded_q)
    embedded_ctx_preds = NestedTimeDist(NestedTimeDist(embed_pred, name='nest1'), name='nest2')(embedded_ctx)
    embed_rule = ZeroGRU(dim, name='embed_rule')
    embedded_rules = NestedTimeDist(embed_rule, name='d_embed_rule')(embedded_ctx_preds)
    repeat_toctx = L.RepeatVector(K.shape(embedded_ctx)[1], name='repeat_to_ctx')
    diff_sq = L.Lambda((lambda xy: K.square((xy[0] - xy[1]))), output_shape=(None, dim), name='diff_sq')
    mult = L.Multiply()
    concat = L.Lambda((lambda xs: K.concatenate(xs, axis=2)), output_shape=(None, (dim * 5)), name='concat')
    att_dense = L.Dense(1, name='d_att_dense')
    squeeze2 = L.Lambda((lambda x: K.squeeze(x, 2)), name='sequeeze2')
    softmax1 = L.Softmax(axis=1)
    unifier = NestedTimeDist(ZeroGRU(dim, go_backwards=True, name='unifier'), name='dist_unifier')
    dot11 = L.Dot((1, 1))
    state = embedded_predq
    repeated_q = repeat_toctx(embedded_predq)
    outs = list()
    for _ in range(iterations):
        ctx_state = repeat_toctx(state)
        s_s_c = diff_sq([ctx_state, embedded_rules])
        s_m_c = mult([embedded_rules, state])
        sim_vec = concat([s_s_c, s_m_c, ctx_state, embedded_rules, repeated_q])
        sim_vec = att_dense(sim_vec)
        sim_vec = squeeze2(sim_vec)
        sim_vec = softmax1(sim_vec)
        outs.append(sim_vec)
        new_states = unifier(embedded_ctx_preds, initial_state=[state])
        state = dot11([sim_vec, new_states])
    out = L.Dense(1, activation='sigmoid', name='out')(state)
    if ilp:
        return (outs, out)
    elif pca:
        model = Model([context, query], [embedded_rules])
    elif training:
        model = Model([context, query], [out])
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    else:
        model = Model([context, query], (outs + [out]))
    return model

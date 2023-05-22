import numpy as np
import keras.backend as K
import keras.layers as L
from keras.models import Model
from .zerogru import ZeroGRU


def build_model(char_size=27, dim=64, iterations=4, training=True, ilp=False, pca=False):
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
    embed_pred = ZeroGRU(dim, go_backwards=True, return_sequences=True, return_state=True, name='embed_pred')
    (embedded_predqs, embedded_predq) = embed_pred(embedded_q)
    embed_pred.return_sequences = False
    embed_pred.return_state = False
    embedded_rules = L.TimeDistributed(embed_pred, name='rule_embed')(embedded_ctx)
    concatm1 = L.Concatenate(name='concatm1')
    repeat_toqlen = L.RepeatVector(K.shape(embedded_q)[1], name='repeat_toqlen')
    mult_cqi = L.Multiply(name='mult_cqi')
    dense_cqi = L.Dense(dim, name='dense_cqi')
    dense_cais = L.Dense(1, name='dense_cais')
    squeeze2 = L.Lambda((lambda x: K.squeeze(x, 2)), name='sequeeze2')
    softmax1 = L.Softmax(axis=1, name='softmax1')
    dot11 = L.Dot((1, 1), name='dot11')
    repeat_toctx = L.RepeatVector(K.shape(context)[1], name='repeat_toctx')
    memory_dense = L.Dense(dim, name='memory_dense')
    kb_dense = L.Dense(dim, name='kb_dense')
    mult_info = L.Multiply(name='mult_info')
    info_dense = L.Dense(dim, name='info_dense')
    mult_att_dense = L.Multiply(name='mult_att_dense')
    read_att_dense = L.Dense(1, name='read_att_dense')
    mem_info_dense = L.Dense(dim, name='mem_info_dense')
    stack1 = L.Lambda((lambda xs: K.stack(xs, 1)), output_shape=(None, dim), name='stack1')
    mult_self_att = L.Multiply(name='mult_self_att')
    self_att_dense = L.Dense(1, name='self_att_dense')
    misa_dense = L.Dense(dim, use_bias=False, name='misa_dense')
    mi_info_dense = L.Dense(dim, name='mi_info_dense')
    add_mip = L.Lambda((lambda xy: (xy[0] + xy[1])), name='add_mip')
    control_gate = L.Dense(1, activation='sigmoid', name='control_gate')
    gate2 = L.Lambda((lambda xyg: ((xyg[2] * xyg[0]) + ((1 - xyg[2]) * xyg[1]))), name='gate')
    zeros_like = L.Lambda(K.zeros_like, name='zeros_like')
    memory = embedded_predq
    control = zeros_like(memory)
    (pmemories, pcontrols) = ([memory], [control])
    outs = list()
    for i in range(iterations):
        qi = L.Dense(dim, name=('qi' + str(i)))(embedded_predq)
        cqi = dense_cqi(concatm1([control, qi]))
        cais = dense_cais(mult_cqi([repeat_toqlen(cqi), embedded_predqs]))
        cais = squeeze2(cais)
        cais = softmax1(cais)
        outs.append(cais)
        new_control = dot11([cais, embedded_predqs])
        info = mult_info([repeat_toctx(memory_dense(memory)), kb_dense(embedded_rules)])
        infop = info_dense(concatm1([info, embedded_rules]))
        rai = read_att_dense(mult_att_dense([repeat_toctx(new_control), infop]))
        rai = squeeze2(rai)
        rai = softmax1(rai)
        outs.append(rai)
        read = dot11([rai, embedded_rules])
        mi_info = mem_info_dense(concatm1([read, memory]))
        past_ctrls = stack1(pcontrols)
        sai = self_att_dense(mult_self_att([L.RepeatVector((i + 1))(new_control), past_ctrls]))
        sai = squeeze2(sai)
        sai = softmax1(sai)
        outs.append(sai)
        past_mems = stack1(pmemories)
        misa = L.dot([sai, past_mems], (1, 1), name=('misa_' + str(i)))
        mip = add_mip([misa_dense(misa), mi_info_dense(mi_info)])
        cip = control_gate(new_control)
        outs.append(cip)
        new_memory = gate2([mip, memory, cip])
        pcontrols.append(new_control)
        pmemories.append(new_memory)
        (memory, control) = (new_memory, new_control)
    out = L.Dense(1, activation='sigmoid', name='out')(concatm1([embedded_predq, memory]))
    if training:
        model = Model([context, query], out)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    else:
        model = Model([context, query], (outs + [out]))
    return model

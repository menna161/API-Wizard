import keras.layers as L
import keras.backend as K
from keras.models import Model


def build_model(char_size=27, dim=64, training=True, **kwargs):
    'Build the model.'
    context = L.Input(shape=(None, None, None), name='context', dtype='int32')
    query = L.Input(shape=(None,), name='query', dtype='int32')
    var_flat = L.Lambda((lambda x: K.reshape(x, K.stack([(- 1), K.prod(K.shape(x)[1:])]))), name='var_flat')
    flat_ctx = var_flat(context)
    onehot = L.Embedding(char_size, char_size, embeddings_initializer='identity', trainable=False, mask_zero=True, name='onehot')
    embedded_ctx = onehot(flat_ctx)
    embedded_q = onehot(query)
    (_, *states) = L.LSTM(dim, return_state=True, name='query_lstm')(embedded_q)
    (out, *states) = L.LSTM(dim, return_state=True, name='ctx_lstm')(embedded_ctx, initial_state=states)
    out = L.concatenate(([out] + states), name='final_states')
    out = L.Dense(1, activation='sigmoid', name='out')(out)
    model = Model([context, query], out)
    if training:
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    return model

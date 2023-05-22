from tensorflow import keras
from keras_embed_sim import EmbeddingRet, EmbeddingSim
from keras_pos_embd import PositionEmbedding
from keras_layer_normalization import LayerNormalization
from keras_transformer import gelu, attention_builder, feed_forward_builder
from keras_transformer import get_custom_objects as get_transformer_custom_objects


def get_model(n_vocab, n_ctx=1024, n_embd=768, n_head=12, n_layer=12, batch_size=None, fixed_input_shape=False):
    'Get basic GPT-2 model.\n\n    :param n_vocab: Number of vocabulary tokens.\n    :param n_ctx: The length of each input.\n    :param n_embd: The dimension of embeddings.\n    :param n_head: Number of heads in transformer.\n    :param n_layer: Number of transformer blocks.\n    :param batch_size: Batch size of the model.\n    :param fixed_input_shape: Whether the length of input is fixed. (Needed for TPU training)\n    :return: The model.\n    '
    if fixed_input_shape:
        input_layer_shape = (batch_size, n_ctx)
    else:
        input_layer_shape = (batch_size, None)
    input_layer = keras.layers.Input(batch_shape=input_layer_shape, name='Input')
    (embed_token, embeddings) = EmbeddingRet(input_dim=n_vocab, output_dim=n_embd, mask_zero=False, name='Embed-Token')(input_layer)
    embed_token_pos = PositionEmbedding(input_dim=n_ctx, output_dim=n_embd, mode=PositionEmbedding.MODE_ADD, name='Embed-Token-Pos')(embed_token)
    last_layer = embed_token_pos
    for i in range(n_layer):
        last_layer = _get_encoder_component(name=('Encode-%d' % i), input_layer=last_layer, head_num=n_head, hidden_dim=(n_embd * 4), attention_activation=None, feed_forward_activation=gelu)
    norm_layer = LayerNormalization(name='Norm')(last_layer)
    output_layer = EmbeddingSim(use_bias=False, name='Output')([norm_layer, embeddings])
    model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.sparse_categorical_crossentropy)
    return model

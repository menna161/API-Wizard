import numpy as np
from tensorflow import keras
from keras_layer_normalization import LayerNormalization
from keras_multi_head import MultiHeadAttention
from keras_position_wise_feed_forward import FeedForward
from keras_pos_embd import TrigPosEmbedding
from keras_embed_sim import EmbeddingRet, EmbeddingSim
from .gelu import gelu


def get_model(token_num, embed_dim, encoder_num, decoder_num, head_num, hidden_dim, attention_activation=None, feed_forward_activation=gelu, dropout_rate=0.0, use_same_embed=True, embed_weights=None, embed_trainable=None, trainable=True):
    'Get full model without compilation.\n\n    :param token_num: Number of distinct tokens.\n    :param embed_dim: Dimension of token embedding.\n    :param encoder_num: Number of encoder components.\n    :param decoder_num: Number of decoder components.\n    :param head_num: Number of heads in multi-head self-attention.\n    :param hidden_dim: Hidden dimension of feed forward layer.\n    :param attention_activation: Activation for multi-head self-attention.\n    :param feed_forward_activation: Activation for feed-forward layer.\n    :param dropout_rate: Dropout rate.\n    :param use_same_embed: Whether to use the same token embedding layer. `token_num`, `embed_weights` and\n                           `embed_trainable` should be lists of two elements if it is False.\n    :param embed_weights: Initial weights of token embedding.\n    :param embed_trainable: Whether the token embedding is trainable. It will automatically set to False if the given\n                            value is None when embedding weights has been provided.\n    :param trainable: Whether the layers are trainable.\n    :return: Keras model.\n    '
    if (not isinstance(token_num, list)):
        token_num = [token_num, token_num]
    (encoder_token_num, decoder_token_num) = token_num
    if (not isinstance(embed_weights, list)):
        embed_weights = [embed_weights, embed_weights]
    (encoder_embed_weights, decoder_embed_weights) = embed_weights
    if (encoder_embed_weights is not None):
        encoder_embed_weights = [encoder_embed_weights]
    if (decoder_embed_weights is not None):
        decoder_embed_weights = [decoder_embed_weights]
    if (not isinstance(embed_trainable, list)):
        embed_trainable = [embed_trainable, embed_trainable]
    (encoder_embed_trainable, decoder_embed_trainable) = embed_trainable
    if (encoder_embed_trainable is None):
        encoder_embed_trainable = (encoder_embed_weights is None)
    if (decoder_embed_trainable is None):
        decoder_embed_trainable = (decoder_embed_weights is None)
    if use_same_embed:
        encoder_embed_layer = decoder_embed_layer = EmbeddingRet(input_dim=encoder_token_num, output_dim=embed_dim, mask_zero=True, weights=encoder_embed_weights, trainable=encoder_embed_trainable, name='Token-Embedding')
    else:
        encoder_embed_layer = EmbeddingRet(input_dim=encoder_token_num, output_dim=embed_dim, mask_zero=True, weights=encoder_embed_weights, trainable=encoder_embed_trainable, name='Encoder-Token-Embedding')
        decoder_embed_layer = EmbeddingRet(input_dim=decoder_token_num, output_dim=embed_dim, mask_zero=True, weights=decoder_embed_weights, trainable=decoder_embed_trainable, name='Decoder-Token-Embedding')
    encoder_input = keras.layers.Input(shape=(None,), name='Encoder-Input')
    encoder_embed = TrigPosEmbedding(mode=TrigPosEmbedding.MODE_ADD, name='Encoder-Embedding')(encoder_embed_layer(encoder_input)[0])
    encoded_layer = get_encoders(encoder_num=encoder_num, input_layer=encoder_embed, head_num=head_num, hidden_dim=hidden_dim, attention_activation=attention_activation, feed_forward_activation=feed_forward_activation, dropout_rate=dropout_rate, trainable=trainable)
    decoder_input = keras.layers.Input(shape=(None,), name='Decoder-Input')
    (decoder_embed, decoder_embed_weights) = decoder_embed_layer(decoder_input)
    decoder_embed = TrigPosEmbedding(mode=TrigPosEmbedding.MODE_ADD, name='Decoder-Embedding')(decoder_embed)
    decoded_layer = get_decoders(decoder_num=decoder_num, input_layer=decoder_embed, encoded_layer=encoded_layer, head_num=head_num, hidden_dim=hidden_dim, attention_activation=attention_activation, feed_forward_activation=feed_forward_activation, dropout_rate=dropout_rate, trainable=trainable)
    output_layer = EmbeddingSim(trainable=trainable, name='Decoder-Output')([decoded_layer, decoder_embed_weights])
    return keras.models.Model(inputs=[encoder_input, decoder_input], outputs=output_layer)

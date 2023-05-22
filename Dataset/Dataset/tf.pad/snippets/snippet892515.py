from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
import thumt.interface as interface
import thumt.layers as layers
from tensorflow.contrib import rnn


def decoding_graph(features, state, mode, params):
    if (mode != 'train'):
        params.residual_dropout = 0.0
        params.attention_dropout = 0.0
        params.relu_dropout = 0.0
        params.label_smoothing = 0.0
    tgt_seq = features['target']
    src_len = features['source_length']
    tgt_len = features['target_length']
    ctx_len = features['context_length']
    src_mask = tf.sequence_mask(src_len, maxlen=tf.shape(features['source'])[1], dtype=tf.float32)
    tgt_mask = tf.sequence_mask(tgt_len, maxlen=tf.shape(features['target'])[1], dtype=tf.float32)
    ctx_mask = tf.sequence_mask(ctx_len, maxlen=tf.shape(features['context'])[1], dtype=tf.float32)
    hidden_size = params.hidden_size
    tvocab = params.vocabulary['target']
    tgt_vocab_size = len(tvocab)
    initializer = tf.random_normal_initializer(0.0, (params.hidden_size ** (- 0.5)))
    if params.shared_source_target_embedding:
        with tf.variable_scope(tf.get_variable_scope(), reuse=True):
            tgt_embedding = tf.get_variable('weights', [tgt_vocab_size, hidden_size], initializer=initializer, trainable=False)
    else:
        tgt_embedding = tf.get_variable('target_embedding', [tgt_vocab_size, hidden_size], initializer=initializer, trainable=False)
    if params.shared_embedding_and_softmax_weights:
        weights = tgt_embedding
    else:
        weights = tf.get_variable('softmax', [tgt_vocab_size, hidden_size], initializer=initializer, trainable=False)
    targets = (tf.gather(tgt_embedding, tgt_seq) * (hidden_size ** 0.5))
    targets = (targets * tf.expand_dims(tgt_mask, (- 1)))
    enc_attn_bias = layers.attention.attention_bias(src_mask, 'masking')
    ctx_attn_bias = layers.attention.attention_bias(ctx_mask, 'masking')
    dec_attn_bias = layers.attention.attention_bias(tf.shape(targets)[1], 'causal')
    decoder_input = tf.pad(targets, [[0, 0], [1, 0], [0, 0]])[(:, :(- 1), :)]
    decoder_input = layers.attention.add_timing_signal(decoder_input)
    if params.residual_dropout:
        keep_prob = (1.0 - params.residual_dropout)
        decoder_input = tf.nn.dropout(decoder_input, keep_prob)
    encoder_output = state['encoder']
    context_output = state['context']
    if (mode != 'infer'):
        if params.context_decoder_attention:
            decoder_output = transformer_decoder(decoder_input, encoder_output, context_output, dec_attn_bias, enc_attn_bias, ctx_attn_bias, params)
        else:
            decoder_output = transformer_decoder(decoder_input, encoder_output, None, dec_attn_bias, enc_attn_bias, None, params)
    else:
        decoder_input = decoder_input[(:, (- 1):, :)]
        dec_attn_bias = dec_attn_bias[(:, :, (- 1):, :)]
        decoder_outputs = transformer_decoder(decoder_input, encoder_output, context_output, dec_attn_bias, enc_attn_bias, ctx_attn_bias, params, state=state['decoder'])
        (decoder_output, decoder_state) = decoder_outputs
        decoder_output = decoder_output[(:, (- 1), :)]
        logits = tf.matmul(decoder_output, weights, False, True)
        log_prob = tf.nn.log_softmax(logits)
        return (log_prob, {'encoder': encoder_output, 'decoder': decoder_state, 'context': context_output})
    decoder_output = tf.reshape(decoder_output, [(- 1), hidden_size])
    logits = tf.matmul(decoder_output, weights, False, True)
    labels = features['target']
    ce = layers.nn.smoothed_softmax_cross_entropy_with_logits(logits=logits, labels=labels, smoothing=params.label_smoothing, normalize=True)
    ce = tf.reshape(ce, tf.shape(tgt_seq))
    if (mode == 'eval'):
        return (- tf.reduce_sum((ce * tgt_mask), axis=1))
    loss = (tf.reduce_sum((ce * tgt_mask)) / tf.reduce_sum(tgt_mask))
    return loss

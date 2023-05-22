from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
import thumt.interface as interface
import thumt.layers as layers


def model_graph(features, mode, params):
    src_vocab_size = len(params.vocabulary['source'])
    tgt_vocab_size = len(params.vocabulary['target'])
    with tf.variable_scope('source_embedding'):
        src_emb = tf.get_variable('embedding', [src_vocab_size, params.embedding_size])
        src_bias = tf.get_variable('bias', [params.embedding_size])
        src_inputs = tf.nn.embedding_lookup(src_emb, features['source'])
    with tf.variable_scope('target_embedding'):
        tgt_emb = tf.get_variable('embedding', [tgt_vocab_size, params.embedding_size])
        tgt_bias = tf.get_variable('bias', [params.embedding_size])
        tgt_inputs = tf.nn.embedding_lookup(tgt_emb, features['target'])
    src_inputs = tf.nn.bias_add(src_inputs, src_bias)
    tgt_inputs = tf.nn.bias_add(tgt_inputs, tgt_bias)
    if (params.dropout and (not params.use_variational_dropout)):
        src_inputs = tf.nn.dropout(src_inputs, (1.0 - params.dropout))
        tgt_inputs = tf.nn.dropout(tgt_inputs, (1.0 - params.dropout))
    cell_fw = layers.rnn_cell.LegacyGRUCell(params.hidden_size)
    cell_bw = layers.rnn_cell.LegacyGRUCell(params.hidden_size)
    if params.use_variational_dropout:
        cell_fw = tf.nn.rnn_cell.DropoutWrapper(cell_fw, input_keep_prob=(1.0 - params.dropout), output_keep_prob=(1.0 - params.dropout), state_keep_prob=(1.0 - params.dropout), variational_recurrent=True, input_size=params.embedding_size, dtype=tf.float32)
        cell_bw = tf.nn.rnn_cell.DropoutWrapper(cell_bw, input_keep_prob=(1.0 - params.dropout), output_keep_prob=(1.0 - params.dropout), state_keep_prob=(1.0 - params.dropout), variational_recurrent=True, input_size=params.embedding_size, dtype=tf.float32)
    encoder_output = _encoder(cell_fw, cell_bw, src_inputs, features['source_length'])
    cell = layers.rnn_cell.LegacyGRUCell(params.hidden_size)
    if params.use_variational_dropout:
        cell = tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=(1.0 - params.dropout), output_keep_prob=(1.0 - params.dropout), state_keep_prob=(1.0 - params.dropout), variational_recurrent=True, input_size=(params.embedding_size + (2 * params.hidden_size)), dtype=tf.float32)
    length = {'source': features['source_length'], 'target': features['target_length']}
    initial_state = encoder_output['final_states']['backward']
    decoder_output = _decoder(cell, tgt_inputs, encoder_output['annotation'], length, initial_state)
    shifted_tgt_inputs = tf.pad(tgt_inputs, [[0, 0], [1, 0], [0, 0]])
    shifted_tgt_inputs = shifted_tgt_inputs[(:, :(- 1), :)]
    all_outputs = tf.concat([tf.expand_dims(decoder_output['initial_state'], axis=1), decoder_output['outputs']], axis=1)
    shifted_outputs = all_outputs[(:, :(- 1), :)]
    maxout_features = [shifted_tgt_inputs, shifted_outputs, decoder_output['values']]
    maxout_size = (params.hidden_size // params.maxnum)
    if (mode is 'infer'):
        maxout_features = [shifted_tgt_inputs[(:, (- 1), :)], shifted_outputs[(:, (- 1), :)], decoder_output['values'][(:, (- 1), :)]]
        maxhid = layers.nn.maxout(maxout_features, maxout_size, params.maxnum, concat=False)
        readout = layers.nn.linear(maxhid, params.embedding_size, False, False, scope='deepout')
        logits = layers.nn.linear(readout, tgt_vocab_size, True, False, scope='softmax')
        return tf.nn.log_softmax(logits)
    maxhid = layers.nn.maxout(maxout_features, maxout_size, params.maxnum, concat=False)
    readout = layers.nn.linear(maxhid, params.embedding_size, False, False, scope='deepout')
    if (params.dropout and (not params.use_variational_dropout)):
        readout = tf.nn.dropout(readout, (1.0 - params.dropout))
    logits = layers.nn.linear(readout, tgt_vocab_size, True, False, scope='softmax')
    logits = tf.reshape(logits, [(- 1), tgt_vocab_size])
    labels = features['target']
    ce = layers.nn.smoothed_softmax_cross_entropy_with_logits(logits=logits, labels=labels, smoothing=params.label_smoothing, normalize=True)
    ce = tf.reshape(ce, tf.shape(labels))
    tgt_mask = tf.to_float(tf.sequence_mask(features['target_length'], maxlen=tf.shape(features['target'])[1]))
    if (mode == 'eval'):
        return (- tf.reduce_sum((ce * tgt_mask), axis=1))
    loss = (tf.reduce_sum((ce * tgt_mask)) / tf.reduce_sum(tgt_mask))
    return loss

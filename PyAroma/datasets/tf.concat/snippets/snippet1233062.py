import loss_computer
import tensorflow as tf


def __call__(self, targets, logits, seq_length):
    multi_targets = targets['multi_targets']
    nr_act_spk = multi_targets.get_shape()[(- 1)]
    logits = logits['act_logit']
    logits = tf.squeeze(logits, axis=(- 1))
    nr_spk = logits.get_shape()[1]
    batch_size = logits.get_shape()[0]
    if (self.lossconf['activation'] == 'sigmoid'):
        logits = tf.sigmoid(logits)
    else:
        raise BaseException('Other activations not yet implemented')
    if (len(logits.get_shape()) != 3):
        raise BaseException('Hardcoded some stuff for 3 dimensions')
    second_dim = logits.get_shape()[1]
    seq_length = seq_length['features']
    max_len = tf.shape(logits)[(- 1)]
    tmp = []
    for utt_ind in range(batch_size):
        tmp.append(tf.expand_dims(tf.concat([tf.ones([second_dim, seq_length[utt_ind]]), tf.zeros([second_dim, (max_len - seq_length[utt_ind])])], (- 1)), 0))
    seq_length_mask = tf.concat(tmp, 0)
    logits = (logits * seq_length_mask)
    if (self.lossconf['av_time'] == 'True'):
        logits = tf.reduce_sum(logits, 2)
        logits = tf.divide(logits, tf.expand_dims(tf.to_float(seq_length), (- 1)))
    targets = tf.concat([tf.ones([batch_size, nr_act_spk]), tf.zeros([batch_size, (nr_spk - nr_act_spk)])], (- 1))
    loss = tf.reduce_sum(tf.square((logits - targets)))
    norm = tf.to_float((batch_size * nr_spk))
    return (loss, norm)

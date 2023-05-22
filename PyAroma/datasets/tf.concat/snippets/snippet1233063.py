import loss_computer
import tensorflow as tf


def oldcall(self, targets, logits, seq_length):
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
    if (self.lossconf['av_time'] == 'True'):
        logits = tf.reduce_mean(logits, 2)
    targets = tf.concat([tf.ones([batch_size, nr_act_spk]), tf.zeros([batch_size, (nr_spk - nr_act_spk)])], (- 1))
    loss = tf.reduce_sum(tf.square((logits - targets)))
    norm = tf.to_float((batch_size * nr_spk))
    return (loss, norm)

import tensorflow as tf
import model
from nabu.neuralnetworks.components import layer
import numpy as np


def permute_versions(replicas, actual_outputs, sequence_length, t_reset, previous_t_reset, group_size, previous_group_size, forward_reset=True, backward_reset=True, separate_directions=False):
    forward_output = actual_outputs[0]
    backward_output = actual_outputs[1]
    forward_replicas = replicas[0]
    backward_replicas = replicas[1]
    batch_size = forward_output.get_shape()[0]
    max_length = tf.shape(forward_output)[1]
    int_dtype = sequence_length.dtype
    if ((np.mod(t_reset, group_size) != 0) or (np.mod(previous_t_reset, previous_group_size) != 0)):
        raise ValueError('Reset period must be multiple of group size')
    num_replicas = int((float(t_reset) / float(group_size)))
    previous_num_replicas = int((float(previous_t_reset) / float(previous_group_size)))
    T = tf.expand_dims(tf.expand_dims(sequence_length, (- 1)), (- 1))
    numbers_to_maxT = tf.range(0, max_length)
    numbers_to_maxT = tf.expand_dims(tf.expand_dims(numbers_to_maxT, 0), (- 1))
    numbers_to_maxT = tf.tile(numbers_to_maxT, [batch_size, 1, num_replicas])
    reversed_numbers_to_maxT = ((T - 1) - numbers_to_maxT)
    numbers_to_k = tf.expand_dims(tf.expand_dims(range(0, num_replicas), 0), 0)
    numbers_to_k = tf.tile(numbers_to_k, [batch_size, max_length, 1])
    max_tau = (previous_t_reset - 1)
    max_tau = np.expand_dims(np.expand_dims(np.expand_dims(max_tau, (- 1)), (- 1)), (- 1))
    max_tau_tf = tf.tile(tf.constant(max_tau, dtype=int_dtype), [batch_size, max_length, num_replicas])
    tau_forward = tf.mod((numbers_to_maxT - (group_size * numbers_to_k)), t_reset)
    tau_forward = tf.minimum(tau_forward, max_tau_tf)
    tau_backward = tf.mod((reversed_numbers_to_maxT - (group_size * numbers_to_k)), t_reset)
    tau_backward = tf.minimum(tau_backward, max_tau_tf)
    forward_indices_for_forward = tf.cast(tf.mod(tf.ceil(tf.truediv((numbers_to_maxT - tau_forward), previous_group_size)), previous_num_replicas), int_dtype)
    backward_indices_for_forward = tf.cast(tf.mod(tf.ceil(tf.truediv((reversed_numbers_to_maxT - tau_forward), previous_group_size)), previous_num_replicas), int_dtype)
    backward_indices_for_backward = tf.cast(tf.mod(tf.ceil(tf.truediv((reversed_numbers_to_maxT - tau_backward), previous_group_size)), previous_num_replicas), int_dtype)
    forward_indices_for_backward = tf.cast(tf.mod(tf.ceil(tf.truediv((numbers_to_maxT - tau_backward), previous_group_size)), previous_num_replicas), int_dtype)
    ra1 = tf.range(batch_size)
    ra1 = tf.expand_dims(tf.expand_dims(ra1, (- 1)), (- 1))
    ra1 = tf.tile(ra1, [1, max_length, num_replicas])
    ra2 = tf.range(max_length)
    ra2 = tf.expand_dims(tf.expand_dims(ra2, 0), (- 1))
    ra2 = tf.tile(ra2, [batch_size, 1, num_replicas])
    stacked_forward_indices_for_forward = tf.stack([ra1, ra2, forward_indices_for_forward], axis=(- 1))
    stacked_backward_indices_for_forward = tf.stack([ra1, ra2, backward_indices_for_forward], axis=(- 1))
    stacked_forward_indices_for_backward = tf.stack([ra1, ra2, forward_indices_for_backward], axis=(- 1))
    stacked_backward_indices_for_backward = tf.stack([ra1, ra2, backward_indices_for_backward], axis=(- 1))
    if forward_reset:
        forward_for_forward = tf.gather_nd(forward_replicas, stacked_forward_indices_for_forward)
    else:
        forward_for_forward = forward_output
    if backward_reset:
        backward_for_backward = tf.gather_nd(backward_replicas, stacked_backward_indices_for_backward)
    else:
        backward_for_backward = backward_output
    if (forward_reset and backward_reset):
        backward_for_forward = tf.gather_nd(backward_replicas, stacked_backward_indices_for_forward)
        forward_for_backward = tf.gather_nd(forward_replicas, stacked_forward_indices_for_backward)
    elif (forward_reset and (not backward_reset)):
        backward_for_forward = tf.tile(tf.expand_dims(backward_output, (- 2)), [1, 1, num_replicas, 1])
        forward_for_backward = forward_output
    elif ((not forward_reset) and backward_reset):
        backward_for_forward = backward_output
        forward_for_backward = tf.tile(tf.expand_dims(forward_output, (- 2)), [1, 1, num_replicas, 1])
    if separate_directions:
        for_forward = forward_for_forward
        for_backward = backward_for_backward
    else:
        for_forward = tf.concat((forward_for_forward, backward_for_forward), (- 1))
        for_backward = tf.concat((forward_for_backward, backward_for_backward), (- 1))
    return (for_forward, for_backward)

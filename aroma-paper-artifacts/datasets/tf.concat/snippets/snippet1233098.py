import tensorflow as tf
import model
import numpy as np
import itertools


def _get_outputs(self, inputs, input_seq_length=None, is_training=None):
    '\n\t\tpermutes and stacks the inputs\n\n\t\tArgs:\n\t\t\tinputs: the inputs to concatenate, this is a list of\n\t\t\t\t[batch_size x time x ...] tensors and/or [batch_size x ...] tensors\n\t\t\tinput_seq_length: None\n\t\t\tis_training: None\n\n\t\tReturns:\n\t\t\t- outputs, the reshaped input\n\t\t'
    permute_dim = int(self.conf['permute_dim'])
    stack_dim = int(self.conf['stack_dim'])
    if (len(inputs) > 1):
        raise ('The implementation of PermuteStacker expects 1 input and not %d' % len(inputs))
    else:
        input = inputs[0]
    with tf.variable_scope(self.scope):
        permute_dim_size = input.get_shape()[permute_dim]
        permutations = list(itertools.permutations(range(permute_dim_size), permute_dim_size))
        all_inp_perms = [tf.gather(input, perm, axis=permute_dim) for perm in permutations]
        output = tf.concat(all_inp_perms, axis=stack_dim)
    return output

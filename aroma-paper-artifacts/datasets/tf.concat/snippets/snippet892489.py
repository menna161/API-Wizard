from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf


def linear(inputs, output_size, bias, concat=True, dtype=None, scope=None, trainable=True):
    "\n    Linear layer\n    :param inputs: A Tensor or a list of Tensors with shape [batch, input_size]\n    :param output_size: An integer specify the output size\n    :param bias: a boolean value indicate whether to use bias term\n    :param concat: a boolean value indicate whether to concatenate all inputs\n    :param dtype: an instance of tf.DType, the default value is ``tf.float32''\n    :param scope: the scope of this layer, the default value is ``linear''\n    :returns: a Tensor with shape [batch, output_size]\n    :raises RuntimeError: raises ``RuntimeError'' when input sizes do not\n                          compatible with each other\n    "
    with tf.variable_scope(scope, default_name='linear', values=[inputs]):
        if (not isinstance(inputs, (list, tuple))):
            inputs = [inputs]
        input_size = [item.get_shape()[(- 1)].value for item in inputs]
        if (len(inputs) != len(input_size)):
            raise RuntimeError('inputs and input_size unmatched!')
        output_shape = tf.concat([tf.shape(inputs[0])[:(- 1)], [output_size]], axis=0)
        inputs = [tf.reshape(inp, [(- 1), inp.shape[(- 1)].value]) for inp in inputs]
        results = []
        if concat:
            input_size = sum(input_size)
            inputs = tf.concat(inputs, 1)
            shape = [input_size, output_size]
            matrix = tf.get_variable('matrix', shape, dtype=dtype, trainable=trainable)
            results.append(tf.matmul(inputs, matrix))
        else:
            for i in range(len(input_size)):
                shape = [input_size[i], output_size]
                name = ('matrix_%d' % i)
                matrix = tf.get_variable(name, shape, dtype=dtype, trainable=trainable)
                results.append(tf.matmul(inputs[i], matrix))
        output = tf.add_n(results)
        if bias:
            shape = [output_size]
            bias = tf.get_variable('bias', shape, dtype=dtype, trainable=trainable)
            output = tf.nn.bias_add(output, bias)
        output = tf.reshape(output, output_shape)
        return output

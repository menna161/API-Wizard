import numpy as np
import tensorflow as tf
from .ops import mu_law_encode, optimizer_factory
from .mixture import discretized_mix_logistic_loss, sample_from_discretized_mix_logistic


def _create_network(self, input_batch, local_condition_batch, global_condition_batch):
    'Construct the WaveNet network.'
    if (self.train_mode == False):
        self._create_queue()
    outputs = []
    current_layer = input_batch
    if (self.train_mode == False):
        self.causal_queue = tf.scatter_update(self.causal_queue, tf.range(self.batch_size), tf.concat([self.causal_queue[(:, 1:, :)], input_batch], axis=1))
        current_layer = self.causal_queue
        self.local_condition_queue = tf.scatter_update(self.local_condition_queue, tf.range(self.batch_size), tf.concat([self.local_condition_queue[(:, 1:, :)], local_condition_batch], axis=1))
        local_condition_batch = self.local_condition_queue
    current_layer = self._create_causal_layer(current_layer)
    if (self.train_mode == True):
        output_width = ((tf.shape(input_batch)[1] - self.receptive_field) + 1)
    else:
        output_width = 1
    with tf.variable_scope('dilated_stack'):
        for (layer_index, dilation) in enumerate(self.dilations):
            with tf.variable_scope('layer{}'.format(layer_index)):
                if (self.train_mode == False):
                    self.dilation_queue[layer_index] = tf.scatter_update(self.dilation_queue[layer_index], tf.range(self.batch_size), tf.concat([self.dilation_queue[layer_index][(:, 1:, :)], current_layer], axis=1))
                    current_layer = self.dilation_queue[layer_index]
                (output, current_layer) = self._create_dilation_layer(current_layer, layer_index, dilation, local_condition_batch, global_condition_batch, output_width)
                outputs.append(output)
    with tf.name_scope('postprocessing'):
        total = sum(outputs)
        transformed1 = tf.nn.relu(total)
        conv1 = tf.layers.conv1d(transformed1, filters=self.skip_channels, kernel_size=1, padding='same', use_bias=self.use_biases)
        transformed2 = tf.nn.relu(conv1)
        if self.scalar_input:
            conv2 = tf.layers.conv1d(transformed2, filters=self.out_channels, kernel_size=1, padding='same', use_bias=self.use_biases)
        else:
            conv2 = tf.layers.conv1d(transformed2, filters=self.quantization_channels, kernel_size=1, padding='same', use_bias=self.use_biases)
    return conv2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import argparse
import json
import glob
import random
import collections
import math
import time
from lxml import etree
from random import shuffle


def create_generator(generator_inputs, generator_outputs_channels):
    print(('generator_inputs :' + str(generator_inputs.get_shape())))
    print(('generator_outputs_channels :' + str(generator_outputs_channels)))
    layers = []
    (inputMean, inputVariance) = tf.nn.moments(generator_inputs, axes=[1, 2], keep_dims=False)
    globalNetworkInput = inputMean
    globalNetworkOutputs = []
    with tf.variable_scope('globalNetwork_fc_1'):
        globalNetwork_fc_1 = fullyConnected(globalNetworkInput, (a.ngf * 2), True, ('globalNetworkLayer' + str((len(globalNetworkOutputs) + 1))))
        globalNetworkOutputs.append(tf.nn.selu(globalNetwork_fc_1))
    with tf.variable_scope('encoder_1'):
        output = conv(generator_inputs, (a.ngf * a.depthFactor), stride=2)
        layers.append(output)
    layer_specs = [((a.ngf * 2) * a.depthFactor), ((a.ngf * 4) * a.depthFactor), ((a.ngf * 8) * a.depthFactor), ((a.ngf * 8) * a.depthFactor), ((a.ngf * 8) * a.depthFactor), ((a.ngf * 8) * a.depthFactor)]
    for (layerCount, out_channels) in enumerate(layer_specs):
        with tf.variable_scope(('encoder_%d' % (len(layers) + 1))):
            rectified = lrelu(layers[(- 1)], 0.2)
            convolved = conv(rectified, out_channels, stride=2)
            (outputs, mean, variance) = instancenorm(convolved)
            outputs = (outputs + GlobalToGenerator(globalNetworkOutputs[(- 1)], out_channels))
            with tf.variable_scope(('globalNetwork_fc_%d' % (len(globalNetworkOutputs) + 1))):
                nextGlobalInput = tf.concat([tf.expand_dims(tf.expand_dims(globalNetworkOutputs[(- 1)], axis=1), axis=1), mean], axis=(- 1))
                globalNetwork_fc = ''
                if ((layerCount + 1) < (len(layer_specs) - 1)):
                    globalNetwork_fc = fullyConnected(nextGlobalInput, layer_specs[(layerCount + 1)], True, ('globalNetworkLayer' + str((len(globalNetworkOutputs) + 1))))
                else:
                    globalNetwork_fc = fullyConnected(nextGlobalInput, layer_specs[layerCount], True, ('globalNetworkLayer' + str((len(globalNetworkOutputs) + 1))))
                globalNetworkOutputs.append(tf.nn.selu(globalNetwork_fc))
            layers.append(outputs)
    with tf.variable_scope('encoder_8'):
        rectified = lrelu(layers[(- 1)], 0.2)
        convolved = conv(rectified, ((a.ngf * 8) * a.depthFactor), stride=2)
        convolved = (convolved + GlobalToGenerator(globalNetworkOutputs[(- 1)], ((a.ngf * 8) * a.depthFactor)))
        with tf.variable_scope(('globalNetwork_fc_%d' % (len(globalNetworkOutputs) + 1))):
            (mean, variance) = tf.nn.moments(convolved, axes=[1, 2], keep_dims=True)
            nextGlobalInput = tf.concat([tf.expand_dims(tf.expand_dims(globalNetworkOutputs[(- 1)], axis=1), axis=1), mean], axis=(- 1))
            globalNetwork_fc = fullyConnected(nextGlobalInput, ((a.ngf * 8) * a.depthFactor), True, ('globalNetworkLayer' + str((len(globalNetworkOutputs) + 1))))
            globalNetworkOutputs.append(tf.nn.selu(globalNetwork_fc))
        layers.append(convolved)
    layer_specs = [(((a.ngf * 8) * a.depthFactor), 0.5), (((a.ngf * 8) * a.depthFactor), 0.5), (((a.ngf * 8) * a.depthFactor), 0.5), (((a.ngf * 8) * a.depthFactor), 0.0), (((a.ngf * 4) * a.depthFactor), 0.0), (((a.ngf * 2) * a.depthFactor), 0.0), ((a.ngf * a.depthFactor), 0.0)]
    num_encoder_layers = len(layers)
    for (decoder_layer, (out_channels, dropout)) in enumerate(layer_specs):
        skip_layer = ((num_encoder_layers - decoder_layer) - 1)
        with tf.variable_scope(('decoder_%d' % (skip_layer + 1))):
            if (decoder_layer == 0):
                input = layers[(- 1)]
            else:
                input = tf.concat([layers[(- 1)], layers[skip_layer]], axis=3)
            rectified = lrelu(input, 0.2)
            output = deconv(rectified, out_channels)
            (output, mean, variance) = instancenorm(output)
            output = (output + GlobalToGenerator(globalNetworkOutputs[(- 1)], out_channels))
            with tf.variable_scope(('globalNetwork_fc_%d' % (len(globalNetworkOutputs) + 1))):
                nextGlobalInput = tf.concat([tf.expand_dims(tf.expand_dims(globalNetworkOutputs[(- 1)], axis=1), axis=1), mean], axis=(- 1))
                globalNetwork_fc = fullyConnected(nextGlobalInput, out_channels, True, ('globalNetworkLayer' + str((len(globalNetworkOutputs) + 1))))
                globalNetworkOutputs.append(tf.nn.selu(globalNetwork_fc))
            if (dropout > 0.0):
                output = tf.nn.dropout(output, keep_prob=(1 - dropout))
            layers.append(output)
    with tf.variable_scope('decoder_1'):
        input = tf.concat([layers[(- 1)], layers[0]], axis=3)
        rectified = lrelu(input, 0.2)
        output = deconv(rectified, generator_outputs_channels)
        output = (output + GlobalToGenerator(globalNetworkOutputs[(- 1)], generator_outputs_channels))
        output = tf.tanh(output)
        layers.append(output)
    return layers[(- 1)]

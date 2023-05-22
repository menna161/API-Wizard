from __future__ import print_function
from collections import defaultdict
import contextlib
import numpy as np
import tensorflow as tf
from tensorflow.python.layers import convolutional as conv_layers
from tensorflow.python.layers import core as core_layers
from tensorflow.python.layers import pooling as pooling_layers
from tensorflow.python.training import moving_averages


def inception_module(self, name, cols, input_layer=None, in_size=None):
    if (input_layer is None):
        input_layer = self.top_layer
    if (in_size is None):
        in_size = self.top_size
    name += str(self.counts[name])
    self.counts[name] += 1
    with tf.variable_scope(name):
        col_layers = []
        col_layer_sizes = []
        for (c, col) in enumerate(cols):
            col_layers.append([])
            col_layer_sizes.append([])
            for (l, layer) in enumerate(col):
                (ltype, args) = (layer[0], layer[1:])
                kwargs = ({'input_layer': input_layer, 'num_channels_in': in_size} if (l == 0) else {})
                if (ltype == 'conv'):
                    self.conv(*args, **kwargs)
                elif (ltype == 'mpool'):
                    self.mpool(*args, **kwargs)
                elif (ltype == 'apool'):
                    self.apool(*args, **kwargs)
                elif (ltype == 'share'):
                    self.top_layer = col_layers[(c - 1)][l]
                    self.top_size = col_layer_sizes[(c - 1)][l]
                else:
                    raise KeyError(("Invalid layer type for inception module: '%s'" % ltype))
                col_layers[c].append(self.top_layer)
                col_layer_sizes[c].append(self.top_size)
        catdim = (3 if (self.data_format == 'NHWC') else 1)
        self.top_layer = tf.concat([layers[(- 1)] for layers in col_layers], catdim)
        self.top_size = sum([sizes[(- 1)] for sizes in col_layer_sizes])
        return self.top_layer

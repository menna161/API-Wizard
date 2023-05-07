import tensorflow as tf
import tensorflow.keras.backend as K
import numpy as np
import os
import time


def call(self, inputs):
    rejoin = (- 1)
    x = inputs
    for layer in self.conv:
        if isinstance(self.conv[layer], tf.keras.layers.Conv2D):
            block = int(layer.split('-')[1])
            if ((block > 0) and (self.shortcuts[(block - 1)] == 1)):
                rejoin = (block + 1)
                y = x
                count_downsampling = ((sum(self.apply_maxpools[block:(block + 2)]) + sum(self.strides[block:(block + 2)])) - 2)
                for _ in range(count_downsampling):
                    y = tf.keras.layers.AveragePooling2D(pool_size=(2, 2))(y)
                y = tf.pad(y, [[0, 0], [0, 0], [0, 0], [0, (self.out_channels[(block + 1)] - self.out_channels[(block - 1)])]], 'CONSTANT')
        if ((block == rejoin) and ('act' in layer)):
            x = tf.keras.layers.Add()([x, y])
        x = self.conv[layer](x)
    x = tf.keras.layers.Flatten()(x)
    for layer in self.mlp:
        x = self.mlp[layer](x)
    return x

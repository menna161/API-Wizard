from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import keras
from keras.layers import Dense, Dropout
from keras.layers import Input, Conv2D, Conv2DTranspose, SeparableConv2D
from keras.layers import ZeroPadding2D, BatchNormalization, Activation
from keras.layers import UpSampling2D
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, LambdaCallback
from keras.models import load_model, Model
from keras.layers.pooling import MaxPooling2D
from keras.utils import plot_model
import numpy as np
import time


def build_model(self):
    dropout = 0.2
    shape = (None, self.ydim, self.xdim, self.channels)
    left = Input(batch_shape=shape)
    right = Input(batch_shape=shape)
    x = SeparableConv2D(filters=16, kernel_size=5, padding='same')(left)
    xleft = SeparableConv2D(filters=1, kernel_size=5, padding='same', dilation_rate=2)(left)
    xin = keras.layers.concatenate([left, right])
    xin = SeparableConv2D(filters=32, kernel_size=5, padding='same')(xin)
    x8 = MaxPooling2D(8)(xin)
    x8 = BatchNormalization()(x8)
    x8 = Activation('relu', name='downsampled_stereo')(x8)
    num_dilations = 4
    dilation_rate = 1
    y = x8
    for i in range(num_dilations):
        a = SeparableConv2D(filters=32, kernel_size=5, padding='same', dilation_rate=dilation_rate)(x8)
        a = Dropout(dropout)(a, training=self.dropout_test)
        y = keras.layers.concatenate([a, y])
        dilation_rate += 1
    dilation_rate = 1
    x = MaxPooling2D(8)(x)
    for i in range(num_dilations):
        x = keras.layers.concatenate([x, y])
        y = BatchNormalization()(x)
        y = Activation('relu')(y)
        y = SeparableConv2D(filters=64, kernel_size=1, padding='same')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)
        y = SeparableConv2D(filters=16, kernel_size=5, padding='same', dilation_rate=dilation_rate)(y)
        y = Dropout(dropout)(y, training=self.dropout_test)
        dilation_rate += 1
    x = keras.layers.concatenate([x, y], name='upsampled_disparity')
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SeparableConv2D(filters=32, kernel_size=1, padding='same')(x)
    x = UpSampling2D(8)(x)
    if (not self.settings.nopadding):
        x = ZeroPadding2D(padding=(2, 0))(x)
    x = keras.layers.concatenate([x, xleft])
    y = BatchNormalization()(x)
    y = Activation('relu')(y)
    y = SeparableConv2D(filters=16, kernel_size=5, padding='same')(y)
    x = keras.layers.concatenate([x, y])
    y = BatchNormalization()(x)
    y = Activation('relu')(y)
    y = Conv2DTranspose(filters=1, kernel_size=9, padding='same')(y)
    self.model = Model([left, right], y)
    if self.settings.model_weights:
        print(('Loading checkpoint model weights %s....' % self.settings.model_weights))
        self.model.load_weights(self.settings.model_weights)
    return self.model

import os
from tensorflow.keras.layers import Dropout, Concatenate, BatchNormalization
from tensorflow.keras.layers import LeakyReLU, Conv2DTranspose, ZeroPadding2D
from tensorflow.keras.layers import Dense, Reshape, Flatten
from tensorflow.keras.layers import Conv2D, ReLU, Input
from tensorflow.keras import Model
from ..datasets.load_pix2pix_datasets import pix2pix_dataloader
from ..losses.pix2pix_loss import pix2pix_generator_loss, pix2pix_discriminator_loss
import imageio
import cv2
import tensorflow as tf
import numpy as np
import datetime
from tqdm.auto import tqdm


def discriminator(self):
    'Discriminator module for Pix2Pix. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    kernel_initializer = self.config['kernel_initializer']
    kernel_size = self.config['kernel_size']
    disc_channels = self.config['disc_channels']
    inputs = Input(shape=self.img_size)
    target = Input(shape=self.img_size)
    x = Concatenate()([inputs, target])
    down_stack = []
    for (i, channel) in enumerate(disc_channels[:(- 1)]):
        if (i == 0):
            down_stack.append(self._downsample(channel, kernel_size=kernel_size, kernel_initializer=kernel_initializer, batchnorm=False))
        else:
            down_stack.append(self._downsample(channel, kernel_size=kernel_size, kernel_initializer=kernel_initializer))
    down_stack.append(ZeroPadding2D())
    down_stack.append(Conv2D(disc_channels[(- 1)], kernel_size=kernel_size, strides=1, kernel_initializer=kernel_initializer, use_bias=False))
    down_stack.append(BatchNormalization())
    down_stack.append(LeakyReLU())
    down_stack.append(ZeroPadding2D())
    last = Conv2D(1, kernel_size=kernel_size, strides=1, kernel_initializer=kernel_initializer)
    for down in down_stack:
        x = down(x)
    out = last(x)
    model = Model(inputs=[inputs, target], outputs=out)
    return model

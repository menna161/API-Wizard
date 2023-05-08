import os
from tensorflow.keras.layers import Dropout, Concatenate, BatchNormalization
from tensorflow.keras.layers import LeakyReLU, Conv2DTranspose, ZeroPadding2D
from tensorflow.keras.layers import Dense, Reshape, Flatten, ReLU
from tensorflow.keras.layers import Input, Conv2D
from tensorflow.keras import Model
from ..losses.minmax_loss import gan_generator_loss, gan_discriminator_loss
from ..losses.cyclegan_loss import cycle_loss, identity_loss
from ..datasets.load_cyclegan_datasets import cyclegan_dataloader
from .pix2pix import Pix2Pix
import tensorflow as tf
import numpy as np
import datetime
import cv2
import imageio
from tqdm.auto import tqdm


def discriminator(self):
    'Discriminator module for CycleGAN. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    kernel_initializer = self.config['kernel_initializer']
    kernel_size = self.config['kernel_size']
    disc_channels = self.config['disc_channels']
    inputs = Input(shape=self.img_size)
    x = inputs
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
    model = Model(inputs=inputs, outputs=out)
    return model

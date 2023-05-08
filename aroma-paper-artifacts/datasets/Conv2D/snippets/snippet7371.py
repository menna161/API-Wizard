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


def generator(self):
    'Generator module for Pix2Pix and CycleGAN(both models use a U-Net as generator). Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    kernel_initializer = self.config['kernel_initializer']
    dropout_rate = self.config['dropout_rate']
    kernel_size = self.config['kernel_size']
    gen_enc_channels = self.config['gen_enc_channels']
    gen_dec_channels = self.config['gen_dec_channels']
    inputs = Input(shape=self.img_size)
    down_stack = [self._downsample((gen_enc_channels[0] // 2), 4, kernel_initializer, batchnorm=False)]
    for channel in gen_enc_channels:
        down_stack.append(self._downsample(channel, kernel_size, kernel_initializer=kernel_initializer))
    up_stack = []
    for (i, channel) in enumerate(gen_dec_channels):
        if (i < 3):
            up_stack.append(self._upsample(channel, kernel_size, kernel_initializer=kernel_initializer, dropout_rate=dropout_rate, dropout=True))
        else:
            up_stack.append(self._upsample(channel, kernel_size, kernel_initializer=kernel_initializer))
    last = Conv2DTranspose(self.channels, strides=2, padding='same', kernel_size=kernel_size, kernel_initializer=kernel_initializer, activation='tanh')
    x = inputs
    skips = []
    for down in down_stack:
        x = down(x)
        skips.append(x)
    skips = reversed(skips[:(- 1)])
    for (up, skip) in zip(up_stack, skips):
        x = up(x)
        x = Concatenate()([x, skip])
    x = last(x)
    model = Model(inputs=inputs, outputs=x)
    return model

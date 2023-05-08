import os
from tensorflow.keras.layers import Conv2D, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.layers import Conv2DTranspose, Dense, Reshape, Flatten
from tensorflow.keras import Model
from ..datasets.load_cifar10 import load_cifar10
from ..datasets.load_mnist import load_mnist
from ..datasets.load_custom_data import load_custom_data
from ..datasets.load_cifar100 import load_cifar100
from ..datasets.load_lsun import load_lsun
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
import cv2
import numpy as np
import datetime
import tensorflow as tf
import imageio
from tqdm.auto import tqdm


def generator(self):
    'Generator module for DCGAN and WGAN. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    noise_dim = self.config['noise_dim']
    gen_channels = self.config['gen_channels']
    gen_layers = len(gen_channels)
    activation = self.config['activation']
    kernel_initializer = self.config['kernel_initializer']
    kernel_regularizer = self.config['kernel_regularizer']
    kernel_size = self.config['kernel_size']
    model = tf.keras.Sequential()
    model.add(Dense((((self.image_size[0] // 4) * (self.image_size[1] // 4)) * (gen_channels[0] * 2)), activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer, input_dim=noise_dim))
    model.add(BatchNormalization())
    model.add(LeakyReLU())
    model.add(Reshape(((self.image_size[0] // 4), (self.image_size[1] // 4), (gen_channels[0] * 2))))
    i = 0
    for _ in range((gen_layers // 2)):
        model.add(Conv2DTranspose(gen_channels[i], kernel_size=kernel_size, strides=(1, 1), padding='same', use_bias=False, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        model.add(BatchNormalization())
        model.add(LeakyReLU())
        i += 1
    model.add(Conv2DTranspose(gen_channels[i], kernel_size=kernel_size, strides=(2, 2), padding='same', use_bias=False, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
    model.add(BatchNormalization())
    model.add(LeakyReLU())
    for _ in range((gen_layers // 2)):
        model.add(Conv2DTranspose(gen_channels[i], kernel_size=kernel_size, strides=(1, 1), padding='same', use_bias=False, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        model.add(BatchNormalization())
        model.add(LeakyReLU())
        i += 1
    model.add(Conv2DTranspose(self.image_size[2], kernel_size=kernel_size, strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    return model

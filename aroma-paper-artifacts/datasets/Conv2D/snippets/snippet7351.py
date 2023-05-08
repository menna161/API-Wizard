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


def discriminator(self):
    'Discriminator module for DCGAN and WGAN. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    dropout_rate = self.config['dropout_rate']
    disc_channels = self.config['disc_channels']
    disc_layers = len(disc_channels)
    kernel_initializer = self.config['kernel_initializer']
    kernel_regularizer = self.config['kernel_regularizer']
    kernel_size = self.config['kernel_size']
    model = tf.keras.Sequential()
    model.add(Conv2D((disc_channels[0] // 2), kernel_size=kernel_size, strides=(2, 2), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer, input_shape=self.image_size))
    model.add(LeakyReLU())
    model.add(Dropout(dropout_rate))
    for i in range(disc_layers):
        model.add(Conv2D(disc_channels[i], kernel_size=kernel_size, strides=(1, 1), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        model.add(LeakyReLU())
        model.add(Dropout(dropout_rate))
    model.add(Conv2D((disc_channels[(- 1)] * 2), kernel_size=kernel_size, strides=(2, 2), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
    model.add(LeakyReLU())
    model.add(Dropout(dropout_rate))
    model.add(Flatten())
    model.add(Dense(1))
    return model

from tensorflow.keras.layers import Conv2D, Dropout, LeakyReLU
from tensorflow.keras.layers import BatchNormalization, Conv2DTranspose
from tensorflow.keras.layers import Dense, Reshape, Flatten, MaxPool2D
import cv2
import imageio
import os
from tensorflow.keras import Model
import numpy as np
from ..datasets.load_cifar10 import load_cifar10_AE
from ..datasets.load_mnist import load_mnist_AE
from ..datasets.load_custom_data import load_custom_data_AE
from ..losses.mse_loss import mse_loss
import tensorflow as tf
import datetime
from tqdm.auto import tqdm


def encoder(self, config):
    enc_channels = config['enc_channels']
    encoder_layers = len(enc_channels)
    interm_dim = config['interm_dim']
    activation = config['activation']
    kernel_initializer = config['kernel_initializer']
    kernel_regularizer = config['kernel_regularizer']
    kernel_size = config['kernel_size']
    model = tf.keras.Sequential()
    model.add(Conv2D((enc_channels[0] // 2), kernel_size=kernel_size, padding='same', activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer, input_shape=self.image_size))
    model.add(MaxPool2D())
    for i in range(encoder_layers):
        model.add(Conv2D(enc_channels[i], kernel_size=kernel_size, padding='same', activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        model.add(MaxPool2D())
    model.add(Flatten())
    model.add(Dense(interm_dim, activation='sigmoid'))
    return model

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


def decoder(self, config):
    dec_channels = config['dec_channels']
    decoder_layers = len(dec_channels)
    interm_dim = config['interm_dim']
    activation = config['activation']
    kernel_initializer = config['kernel_initializer']
    kernel_regularizer = config['kernel_regularizer']
    kernel_size = config['kernel_size']
    model = tf.keras.Sequential()
    model.add(Dense((((self.image_size[0] // 4) * (self.image_size[1] // 4)) * (dec_channels[0] * 2)), activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer, input_dim=interm_dim))
    model.add(Reshape(((self.image_size[0] // 4), (self.image_size[1] // 4), (dec_channels[0] * 2))))
    k = 0
    for _ in range((decoder_layers // 2)):
        model.add(Conv2DTranspose(dec_channels[k], kernel_size=kernel_size, strides=(1, 1), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        k += 1
    model.add(Conv2DTranspose(dec_channels[k], kernel_size=kernel_size, strides=(2, 2), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
    for _ in range((decoder_layers // 2)):
        model.add(Conv2DTranspose(dec_channels[k], kernel_size=kernel_size, strides=(1, 1), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer))
        k += 1
    model.add(Conv2DTranspose(self.image_size[2], kernel_size=kernel_size, strides=(2, 2), padding='same', activation='tanh'))
    return model

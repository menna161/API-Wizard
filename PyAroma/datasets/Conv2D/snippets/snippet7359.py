import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_mnist import load_mnist
from ..datasets.load_cifar10 import load_cifar10
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
from ..losses.infogan_loss import auxillary_loss
import datetime
from tqdm import tqdm
import logging
import imageio


def conv_block(self, inputs, filters, kernel_size, strides=(2, 2), kernel_initializer='glorot_uniform', kernel_regularizer=None, padding='same', activation='leaky_relu', use_batch_norm=True, conv_type='normal'):
    if (conv_type == 'transpose'):
        x = layers.Conv2DTranspose(filters, kernel_size, strides=strides, padding=padding, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer)(inputs)
    else:
        x = layers.Conv2D(filters, kernel_size, strides=strides, padding=padding, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer)(inputs)
    if use_batch_norm:
        x = layers.BatchNormalization()(x)
    if (activation == 'leaky_relu'):
        x = layers.LeakyReLU()(x)
    elif (activation == 'tanh'):
        x = tf.keras.activations.tanh(x)
    return x

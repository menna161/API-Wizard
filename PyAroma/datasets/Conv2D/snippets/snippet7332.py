import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_mnist import load_mnist_with_labels
from ..datasets.load_cifar10 import load_cifar10_with_labels
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
import datetime
import imageio
from tqdm.auto import tqdm


def generator(self):
    'Generator module for Conditional GAN. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    gen_channels = self.config['gen_channels']
    gen_layers = len(gen_channels)
    activation = self.config['activation']
    kernel_initializer = self.config['kernel_initializer']
    kernel_regularizer = self.config['kernel_regularizer']
    kernel_size = self.config['kernel_size']
    z = layers.Input(shape=self.noise_dim)
    label = layers.Input(shape=1)
    start_image_size = ((self.image_size[0] // 4), (self.image_size[1] // 4))
    embedded_label = layers.Embedding(input_dim=self.n_classes, output_dim=self.embed_dim)(label)
    embedded_label = layers.Dense(units=(start_image_size[0] * start_image_size[1]), activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer, input_dim=self.embed_dim)(embedded_label)
    embedded_label = layers.Reshape((start_image_size[0], start_image_size[1], 1))(embedded_label)
    input_img = layers.Dense((((start_image_size[0] * start_image_size[1]) * gen_channels[0]) * 2), activation=activation, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer)(z)
    input_img = layers.Reshape((start_image_size[0], start_image_size[1], (gen_channels[0] * 2)))(input_img)
    x = layers.Concatenate()([input_img, embedded_label])
    for i in range(gen_layers):
        x = layers.Conv2DTranspose(filters=gen_channels[i], kernel_size=kernel_size, strides=(1, 1), padding='same', use_bias=False, kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer)(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU()(x)
    x = layers.Conv2DTranspose(filters=(gen_channels[(- 1)] // 2), kernel_size=kernel_size, strides=(2, 2), padding='same', use_bias=False, activation='tanh')(x)
    x = layers.BatchNormalization()(x)
    x = layers.LeakyReLU()(x)
    output = layers.Conv2DTranspose(filters=self.image_size[(- 1)], kernel_size=kernel_size, strides=(2, 2), padding='same', use_bias=False, activation='tanh')(x)
    model = tf.keras.Model([z, label], output)
    return model

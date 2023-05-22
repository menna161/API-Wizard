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


def discriminator(self):
    'Discriminator module for Conditional GAN. Use it as a regular TensorFlow 2.0 Keras Model.\n\n        Return:\n            A tf.keras model  \n        '
    dropout_rate = self.config['dropout_rate']
    disc_channels = self.config['disc_channels']
    disc_layers = len(disc_channels)
    activation = self.config['activation']
    kernel_initializer = self.config['kernel_initializer']
    kernel_regularizer = self.config['kernel_regularizer']
    kernel_size = self.config['kernel_size']
    input_image = layers.Input(shape=self.image_size)
    input_label = layers.Input(shape=1)
    embedded_label = layers.Embedding(input_dim=self.n_classes, output_dim=self.embed_dim)(input_label)
    embedded_label = layers.Dense(units=(self.image_size[0] * self.image_size[1]), activation=activation)(embedded_label)
    embedded_label = layers.Reshape((self.image_size[0], self.image_size[1], 1))(embedded_label)
    x = layers.Concatenate()([input_image, embedded_label])
    for i in range(disc_layers):
        x = layers.Conv2D(filters=disc_channels[i], kernel_size=kernel_size, strides=(2, 2), padding='same', kernel_initializer=kernel_initializer, kernel_regularizer=kernel_regularizer)(x)
    x = layers.BatchNormalization()(x)
    x = layers.LeakyReLU()(x)
    x = layers.Flatten()(x)
    fe = layers.Dropout(dropout_rate)(x)
    out_layer = layers.Dense(1, activation='sigmoid')(fe)
    model = tf.keras.Model(inputs=[input_image, input_label], outputs=out_layer)
    return model

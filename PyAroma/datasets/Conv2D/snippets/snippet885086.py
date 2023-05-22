from keras.utils import multi_gpu_model
import numpy as np
import tensorflow as tf
import pickle
from keras.models import Model, Input
from keras.optimizers import Adam, RMSprop
from keras.layers import Dense
from keras.layers import Conv2D, Conv2DTranspose
from keras.layers import Flatten, Add
from keras.layers import Concatenate, Activation
from keras.layers import LeakyReLU, BatchNormalization, Lambda
from keras import backend as K
import os


def discriminator(inp_shape=(256, 256, 1), trainable=True):
    gamma_init = tf.random_normal_initializer(1.0, 0.02)
    inp = Input(shape=(256, 256, 1))
    l0 = Conv2D(64, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(inp)
    l0 = LeakyReLU(alpha=0.2)(l0)
    l1 = Conv2D((64 * 2), (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l0)
    l1 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l1)
    l1 = LeakyReLU(alpha=0.2)(l1)
    l2 = Conv2D((64 * 4), (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l1)
    l2 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l2)
    l2 = LeakyReLU(alpha=0.2)(l2)
    l3 = Conv2D((64 * 8), (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l2)
    l3 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l3)
    l3 = LeakyReLU(alpha=0.2)(l3)
    l4 = Conv2D((64 * 16), (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l3)
    l4 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l4)
    l4 = LeakyReLU(alpha=0.2)(l4)
    l5 = Conv2D((64 * 32), (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l4)
    l5 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l5)
    l5 = LeakyReLU(alpha=0.2)(l5)
    l6 = Conv2D((64 * 16), (1, 1), strides=(1, 1), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l5)
    l6 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l6)
    l6 = LeakyReLU(alpha=0.2)(l6)
    l7 = Conv2D((64 * 8), (1, 1), strides=(1, 1), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l6)
    l7 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l7)
    l7 = LeakyReLU(alpha=0.2)(l7)
    l8 = Conv2D((64 * 2), (1, 1), strides=(1, 1), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l7)
    l8 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l8)
    l8 = LeakyReLU(alpha=0.2)(l8)
    l9 = Conv2D((64 * 2), (3, 3), strides=(1, 1), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l8)
    l9 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l9)
    l9 = LeakyReLU(alpha=0.2)(l9)
    l10 = Conv2D((64 * 8), (3, 3), strides=(1, 1), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l9)
    l10 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(l10)
    l10 = LeakyReLU(alpha=0.2)(l10)
    l11 = Add()([l7, l10])
    l11 = LeakyReLU(alpha=0.2)(l11)
    out = Conv2D(filters=1, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(l11)
    model = Model(inputs=inp, outputs=out)
    return model

import tensorflow as tf
import os
from keras.utils import multi_gpu_model
from keras.models import Model, Input
from keras.layers import Conv2D, Conv2DTranspose
from keras.layers import Flatten, Add
from keras.layers import Concatenate, Activation
from keras.layers import LeakyReLU, BatchNormalization, Lambda
import numpy as np
from metrics import metrics
from keras.initializers import constant
import pickle
import time
from keras import backend as K
from tensorflow.python.ops import array_ops
from keras.initializers import RandomUniform


def generator(inp_shape, trainable=True):
    gamma_init = tf.random_normal_initializer(1.0, 0.02)
    fd = 512
    gr = 32
    nb = 12
    betad = 0.2
    betar = 0.2
    inp_real_imag = Input(inp_shape)
    lay_128dn = Conv2D(64, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(inp_real_imag)
    lay_128dn = LeakyReLU(alpha=0.2)(lay_128dn)
    lay_64dn = Conv2D(128, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_128dn)
    lay_64dn = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_64dn)
    lay_64dn = LeakyReLU(alpha=0.2)(lay_64dn)
    lay_32dn = Conv2D(256, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_64dn)
    lay_32dn = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_32dn)
    lay_32dn = LeakyReLU(alpha=0.2)(lay_32dn)
    lay_16dn = Conv2D(512, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_32dn)
    lay_16dn = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_16dn)
    lay_16dn = LeakyReLU(alpha=0.2)(lay_16dn)
    lay_8dn = Conv2D(512, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_16dn)
    lay_8dn = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_8dn)
    lay_8dn = LeakyReLU(alpha=0.2)(lay_8dn)
    xc1 = Conv2D(filters=fd, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_8dn)
    xrrd = xc1
    for m in range(nb):
        xrrd = resresden(xrrd, fd, gr, betad, betar, gamma_init, trainable)
    xc2 = Conv2D(filters=fd, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(xrrd)
    lay_8upc = Add()([xc1, xc2])
    lay_16up = Conv2DTranspose(1024, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_8upc)
    lay_16up = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_16up)
    lay_16up = Activation('relu')(lay_16up)
    lay_16upc = Concatenate(axis=(- 1))([lay_16up, lay_16dn])
    lay_32up = Conv2DTranspose(256, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_16upc)
    lay_32up = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_32up)
    lay_32up = Activation('relu')(lay_32up)
    lay_32upc = Concatenate(axis=(- 1))([lay_32up, lay_32dn])
    lay_64up = Conv2DTranspose(128, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_32upc)
    lay_64up = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_64up)
    lay_64up = Activation('relu')(lay_64up)
    lay_64upc = Concatenate(axis=(- 1))([lay_64up, lay_64dn])
    lay_128up = Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_64upc)
    lay_128up = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_128up)
    lay_128up = Activation('relu')(lay_128up)
    lay_128upc = Concatenate(axis=(- 1))([lay_128up, lay_128dn])
    lay_256up = Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_128upc)
    lay_256up = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(lay_256up)
    lay_256up = Activation('relu')(lay_256up)
    out = Conv2D(1, (1, 1), strides=(1, 1), activation='tanh', padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(lay_256up)
    model = Model(inputs=inp_real_imag, outputs=out)
    return model

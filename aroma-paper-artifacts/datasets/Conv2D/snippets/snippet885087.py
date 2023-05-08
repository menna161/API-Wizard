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


def resden(x, fil, gr, beta, gamma_init, trainable):
    x1 = Conv2D(filters=gr, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(x)
    x1 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(x1)
    x1 = LeakyReLU(alpha=0.2)(x1)
    x1 = Concatenate(axis=(- 1))([x, x1])
    x2 = Conv2D(filters=gr, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(x1)
    x2 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(x2)
    x2 = LeakyReLU(alpha=0.2)(x2)
    x2 = Concatenate(axis=(- 1))([x1, x2])
    x3 = Conv2D(filters=gr, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(x2)
    x3 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(x3)
    x3 = LeakyReLU(alpha=0.2)(x3)
    x3 = Concatenate(axis=(- 1))([x2, x3])
    x4 = Conv2D(filters=gr, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(x3)
    x4 = BatchNormalization(gamma_initializer=gamma_init, trainable=trainable)(x4)
    x4 = LeakyReLU(alpha=0.2)(x4)
    x4 = Concatenate(axis=(- 1))([x3, x4])
    x5 = Conv2D(filters=fil, kernel_size=3, strides=1, padding='same', use_bias=True, kernel_initializer='he_normal', bias_initializer='zeros')(x4)
    x5 = Lambda((lambda x: (x * beta)))(x5)
    xout = Add()([x5, x])
    return xout

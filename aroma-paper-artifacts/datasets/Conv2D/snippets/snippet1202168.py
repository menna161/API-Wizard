import tensorflow as tf
import keras.backend as K
import keras.layers as KL
import keras.models as KM
import os
import numpy as np
import keras.optimizers
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator


def build_model(x_train, num_classes):
    tf.reset_default_graph()
    inputs = KL.Input(shape=x_train.shape[1:], name='input_image')
    x = KL.Conv2D(32, (3, 3), activation='relu', padding='same', name='conv1')(inputs)
    x = KL.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2')(x)
    x = KL.MaxPooling2D(pool_size=(2, 2), name='pool1')(x)
    x = KL.Flatten(name='flat1')(x)
    x = KL.Dense(128, activation='relu', name='dense1')(x)
    x = KL.Dense(num_classes, activation='softmax', name='dense2')(x)
    return KM.Model(inputs, x, 'digit_classifier_model')

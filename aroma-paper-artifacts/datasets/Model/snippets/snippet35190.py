from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import glob
import itertools
import numpy
import os
import tensorflow
from keras.callbacks import Callback
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.layers import Concatenate
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import Reshape
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import UpSampling2D
from keras.models import Model
from PIL import Image
from utils import TelegramIM


def __new__(self, input_shapes, optimizer, loss, weights=None):
    x1 = Input(input_shapes[0])
    x2 = Input(input_shapes[1])
    y1 = Conv2D(filters=16, kernel_size=(3, 3), padding='same', activation='relu')(x1)
    y1 = Conv2D(filters=16, kernel_size=(3, 3), padding='same', activation='relu')(y1)
    y1 = Conv2D(filters=1, kernel_size=(3, 3), padding='same', activation='relu')(y1)
    y1 = Flatten()(y1)
    y1 = Dense(units=512, activation='relu')(y1)
    y2 = Flatten()(x2)
    y2 = Dense(units=512, activation='relu')(y2)
    y = Concatenate()([y1, y2])
    y = Dense(units=1024, activation='relu')(y)
    y = Dropout(0.5)(y)
    y = Dense(units=1024, activation='relu')(y)
    y = Reshape(target_shape=(8, 8, 16))(y)
    y = UpSampling2D(size=(2, 2))(y)
    y = Conv2D(filters=16, kernel_size=(3, 3), padding='same', activation='relu')(y)
    y = UpSampling2D(size=(2, 2))(y)
    y = Conv2D(filters=16, kernel_size=(3, 3), padding='same', activation='relu')(y)
    y = UpSampling2D(size=(2, 2))(y)
    y = Conv2D(filters=1, kernel_size=(3, 3), padding='same', activation='relu')(y)
    model = Model(inputs=[x1, x2], outputs=y)
    model.compile(optimizer=optimizer, loss=loss)
    try:
        if (not (weights is None)):
            model.load_weights(weights)
    except:
        pass
    return model

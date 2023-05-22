from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense, Dropout
from keras import backend as K
from keras.layers import MaxPooling2D


@staticmethod
def build(width, height, depth, classes):
    model = Sequential()
    input_shape = (height, width, depth)
    if (K.image_data_format() == 'channels_first'):
        input_shape = (depth, height, width)
    model.add(Conv2D(size, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Conv2D(size, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Conv2D(size, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.5))
    model.add(Conv2D(size, (3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Activation('relu'))
    model.add(Dense(classes))
    model.add(Activation('softmax'))
    return model

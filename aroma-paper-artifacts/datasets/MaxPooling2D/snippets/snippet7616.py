from keras.layers.core import Dense, MaxoutDense, Dropout, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential, model_from_json
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.utils.visualize_util import to_graph


def get_convnet():
    model = Sequential()
    model.add(ZeroPadding2D())
    for (filtersize, poolsize) in [(11, 2), (3, 3), (3, 3)]:
        model.add(Dropout(0.2))
        model.add(Convolution2D(32, 1, filtersize, filtersize, W_regularizer=l2()))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(poolsize=(poolsize, poolsize)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Dense(2))
    model.add(Activation('sigmoid'))
    return model

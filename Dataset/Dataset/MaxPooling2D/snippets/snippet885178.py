import numpy as np
import random as rand
import math
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization


def decode(self, genome):
    if (not self.is_compatible_genome(genome)):
        raise ValueError('Invalid genome for specified configs')
    model = Sequential()
    dim = 0
    offset = 0
    if (self.convolution_layers > 0):
        dim = min(self.input_shape[:(- 1)])
    input_layer = True
    for i in range(self.convolution_layers):
        if genome[offset]:
            convolution = None
            if input_layer:
                convolution = Convolution2D(genome[(offset + 1)], (3, 3), padding='same', input_shape=self.input_shape)
                input_layer = False
            else:
                convolution = Convolution2D(genome[(offset + 1)], (3, 3), padding='same')
            model.add(convolution)
            if genome[(offset + 2)]:
                model.add(BatchNormalization())
            model.add(Activation(self.activation[genome[(offset + 3)]]))
            model.add(Dropout(float((genome[(offset + 4)] / 20.0))))
            max_pooling_type = genome[(offset + 5)]
            if ((max_pooling_type == 1) and (dim >= 5)):
                model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
                dim = int(math.ceil((dim / 2)))
        offset += self.convolution_layer_size
    if (not input_layer):
        model.add(Flatten())
    for i in range(self.dense_layers):
        if genome[offset]:
            dense = None
            if input_layer:
                dense = Dense(genome[(offset + 1)], input_shape=self.input_shape)
                input_layer = False
            else:
                dense = Dense(genome[(offset + 1)])
            model.add(dense)
            if genome[(offset + 2)]:
                model.add(BatchNormalization())
            model.add(Activation(self.activation[genome[(offset + 3)]]))
            model.add(Dropout(float((genome[(offset + 4)] / 20.0))))
        offset += self.dense_layer_size
    model.add(Dense(self.n_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=self.optimizer[genome[offset]], metrics=['accuracy'])
    return model

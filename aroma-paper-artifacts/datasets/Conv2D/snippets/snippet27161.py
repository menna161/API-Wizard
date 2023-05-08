import typing
import keras
import keras.backend as K
import tensorflow as tf
from matchzoo import preprocessors
from matchzoo.contrib.layers import DecayingDropoutLayer
from matchzoo.contrib.layers import EncodingLayer
from matchzoo.engine import hyper_spaces
from matchzoo.engine.base_model import BaseModel
from matchzoo.engine.param import Param
from matchzoo.engine.param_table import ParamTable


def _wrapper(x):
    for _ in range(self._params['nb_dense_blocks']):
        for _ in range(self._params['layers_per_dense_block']):
            out_conv = keras.layers.Conv2D(filters=self._params['growth_rate'], kernel_size=(3, 3), padding='same', activation='relu')(x)
            x = keras.layers.Concatenate(axis=(- 1))([x, out_conv])
        scale_down_ratio = self._params['transition_scale_down_ratio']
        nb_filter = int((K.int_shape(x)[(- 1)] * scale_down_ratio))
        x = keras.layers.Conv2D(filters=nb_filter, kernel_size=(1, 1), padding='same', activation=None)(x)
        x = keras.layers.MaxPool2D(strides=(2, 2))(x)
    out_densenet = keras.layers.Flatten()(x)
    return out_densenet

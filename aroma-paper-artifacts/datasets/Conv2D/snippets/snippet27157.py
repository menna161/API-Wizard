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


def build(self):
    'Build model structure.'
    inputs = self._make_inputs()
    (text_left, text_right) = inputs[0:2]
    (char_left, char_right) = inputs[2:4]
    (match_left, match_right) = inputs[4:6]
    left_embeddings = []
    right_embeddings = []
    word_embedding = self._make_embedding_layer()
    left_word_embedding = word_embedding(text_left)
    right_word_embedding = word_embedding(text_right)
    left_word_embedding = DecayingDropoutLayer(initial_keep_rate=self._params['dropout_initial_keep_rate'], decay_interval=self._params['dropout_decay_interval'], decay_rate=self._params['dropout_decay_rate'])(left_word_embedding)
    right_word_embedding = DecayingDropoutLayer(initial_keep_rate=self._params['dropout_initial_keep_rate'], decay_interval=self._params['dropout_decay_interval'], decay_rate=self._params['dropout_decay_rate'])(right_word_embedding)
    left_embeddings.append(left_word_embedding)
    right_embeddings.append(right_word_embedding)
    left_exact_match = keras.layers.Reshape(target_shape=(K.int_shape(match_left)[1], 1))(match_left)
    right_exact_match = keras.layers.Reshape(target_shape=(K.int_shape(match_left)[1], 1))(match_right)
    left_embeddings.append(left_exact_match)
    right_embeddings.append(right_exact_match)
    char_embedding = self._make_char_embedding_layer()
    char_embedding.build(input_shape=(None, None, K.int_shape(char_left)[(- 1)]))
    left_char_embedding = char_embedding(char_left)
    right_char_embedding = char_embedding(char_right)
    left_embeddings.append(left_char_embedding)
    right_embeddings.append(right_char_embedding)
    left_embedding = keras.layers.Concatenate()(left_embeddings)
    right_embedding = keras.layers.Concatenate()(right_embeddings)
    d = K.int_shape(left_embedding)[(- 1)]
    left_encoding = EncodingLayer(initial_keep_rate=self._params['dropout_initial_keep_rate'], decay_interval=self._params['dropout_decay_interval'], decay_rate=self._params['dropout_decay_rate'])(left_embedding)
    right_encoding = EncodingLayer(initial_keep_rate=self._params['dropout_initial_keep_rate'], decay_interval=self._params['dropout_decay_interval'], decay_rate=self._params['dropout_decay_rate'])(right_embedding)
    interaction = keras.layers.Lambda(self._make_interaction)([left_encoding, right_encoding])
    feature_extractor_input = keras.layers.Conv2D(filters=int((d * self._params['first_scale_down_ratio'])), kernel_size=(1, 1), activation=None)(interaction)
    feature_extractor = self._create_densenet()
    features = feature_extractor(feature_extractor_input)
    features = DecayingDropoutLayer(initial_keep_rate=self._params['dropout_initial_keep_rate'], decay_interval=self._params['dropout_decay_interval'], decay_rate=self._params['dropout_decay_rate'])(features)
    out = self._make_output_layer()(features)
    self._backend = keras.Model(inputs=inputs, outputs=out)

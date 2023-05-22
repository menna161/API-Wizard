from . import Submodel
from ... import initializers
from ...losses import focal
from ...utils.config import set_defaults
import tensorflow as tf


def default_classification_model(num_classes, num_anchors, pyramid_feature_size=256, prior_probability=0.01, classification_feature_size=256, name='classification_submodel'):
    ' Creates the default regression submodel.\n\tArgs\n\t\tnum_classes                 : Number of classes to predict a score for at each feature level.\n\t\tnum_anchors                 : Number of anchors to predict classification scores for at each feature level.\n\t\tpyramid_feature_size        : The number of filters to expect from the feature pyramid levels.\n\t\tprior_probability           : Probability for the bias initializer of the last convolutional layer.\n\t\tclassification_feature_size : The number of filters to use in the layers in the classification submodel.\n\t\tname                        : The name of the submodel.\n\tReturns\n\t\tA tensorflow.keras.models.Model that predicts classes for each anchor.\n\t'
    options = {'kernel_size': 3, 'strides': 1, 'padding': 'same'}
    if (tf.keras.backend.image_data_format() == 'channels_first'):
        inputs = tf.keras.layers.Input(shape=(pyramid_feature_size, None, None))
    else:
        inputs = tf.keras.layers.Input(shape=(None, None, pyramid_feature_size))
    outputs = inputs
    for i in range(4):
        outputs = tf.keras.layers.Conv2D(filters=classification_feature_size, activation='relu', name='pyramid_classification_{}'.format(i), kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None), bias_initializer='zeros', **options)(outputs)
    outputs = tf.keras.layers.Conv2D(filters=(num_classes * num_anchors), kernel_initializer=tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None), bias_initializer=initializers.PriorProbability(probability=prior_probability), name='pyramid_classification', **options)(outputs)
    if (tf.keras.backend.image_data_format() == 'channels_first'):
        outputs = tf.keras.layers.Permute((2, 3, 1), name='pyramid_classification_permute')(outputs)
    outputs = tf.keras.layers.Reshape(((- 1), num_classes), name='pyramid_classification_reshape')(outputs)
    outputs = tf.keras.layers.Activation('sigmoid', name='pyramid_classification_sigmoid')(outputs)
    return tf.keras.models.Model(inputs=inputs, outputs=outputs, name=name)

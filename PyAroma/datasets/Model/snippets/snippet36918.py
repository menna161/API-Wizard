from . import Submodel
from ...losses import smooth_l1
import tensorflow as tf
from ...utils.config import set_defaults


def default_regression_model(num_values, num_anchors, pyramid_feature_size=256, regression_feature_size=256, name='regression_submodel'):
    ' Creates the default regression submodel.\n\tArgs\n\t\tnum_values              : Number of values to regress.\n\t\tnum_anchors             : Number of anchors to regress for each feature level.\n\t\tpyramid_feature_size    : The number of filters to expect from the feature pyramid levels.\n\t\tregression_feature_size : The number of filters to use in the layers in the regression submodel.\n\t\tname                    : The name of the submodel.\n\tReturns\n\t\tA tf.keras.models.Model that predicts regression values for each anchor.\n\t'
    options = {'kernel_size': 3, 'strides': 1, 'padding': 'same', 'kernel_initializer': tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None), 'bias_initializer': 'zeros'}
    if (tf.keras.backend.image_data_format() == 'channels_first'):
        inputs = tf.keras.layers.Input(shape=(pyramid_feature_size, None, None))
    else:
        inputs = tf.keras.layers.Input(shape=(None, None, pyramid_feature_size))
    outputs = inputs
    for i in range(4):
        outputs = tf.keras.layers.Conv2D(filters=regression_feature_size, activation='relu', name='pyramid_regression_{}'.format(i), **options)(outputs)
    outputs = tf.keras.layers.Conv2D((num_anchors * num_values), name='pyramid_regression', **options)(outputs)
    if (tf.keras.backend.image_data_format() == 'channels_first'):
        outputs = tf.keras.layers.Permute((2, 3, 1), name='pyramid_regression_permute')(outputs)
    outputs = tf.keras.layers.Reshape(((- 1), num_values), name='pyramid_regression_reshape')(outputs)
    return tf.keras.models.Model(inputs=inputs, outputs=outputs, name=name)

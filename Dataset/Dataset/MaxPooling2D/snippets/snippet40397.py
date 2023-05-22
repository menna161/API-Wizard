from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import warnings
from keras.models import Model
from keras import layers
from keras.layers import Activation
from keras.layers import Dense
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers import GlobalMaxPooling2D
from keras.engine.topology import get_source_inputs
from keras.utils.data_utils import get_file
from keras import backend as K
from keras.applications import imagenet_utils
import keras
from distutils.version import StrictVersion
from keras.applications.imagenet_utils import _obtain_input_shape
from keras_applications.imagenet_utils import _obtain_input_shape


def InceptionV3(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000):
    "Instantiates the Inception v3 architecture.\n    Optionally loads weights pre-trained\n    on ImageNet. Note that when using TensorFlow,\n    for best performance you should set\n    `image_data_format='channels_last'` in your Keras config\n    at ~/.keras/keras.json.\n    The model and the weights are compatible with both\n    TensorFlow and Theano. The data format\n    convention used by the model is the one\n    specified in your Keras config file.\n    Note that the default input image size for this model is 299x299.\n    # Arguments\n        include_top: whether to include the fully-connected\n            layer at the top of the network.\n        weights: one of `None` (random initialization),\n              'imagenet' (pre-training on ImageNet),\n              or the path to the weights file to be loaded.\n        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)\n            to use as image input for the model.\n        input_shape: optional shape tuple, only to be specified\n            if `include_top` is False (otherwise the input shape\n            has to be `(299, 299, 3)` (with `channels_last` data format)\n            or `(3, 299, 299)` (with `channels_first` data format).\n            It should have exactly 3 inputs channels,\n            and width and height should be no smaller than 139.\n            E.g. `(150, 150, 3)` would be one valid value.\n        pooling: Optional pooling mode for feature extraction\n            when `include_top` is `False`.\n            - `None` means that the output of the model will be\n                the 4D tensor output of the\n                last convolutional layer.\n            - `avg` means that global average pooling\n                will be applied to the output of the\n                last convolutional layer, and thus\n                the output of the model will be a 2D tensor.\n            - `max` means that global max pooling will\n                be applied.\n        classes: optional number of classes to classify images\n            into, only to be specified if `include_top` is True, and\n            if no `weights` argument is specified.\n    # Returns\n        A Keras model instance.\n    # Raises\n        ValueError: in case of invalid argument for `weights`,\n            or invalid input shape.\n    "
    if (not ((weights in {'imagenet', None}) or os.path.exists(weights))):
        raise ValueError('The `weights` argument should be either `None` (random initialization), `imagenet` (pre-training on ImageNet), or the path to the weights file to be loaded.')
    if ((weights == 'imagenet') and include_top and (classes != 1000)):
        raise ValueError('If using `weights` as imagenet with `include_top` as true, `classes` should be 1000')
    input_shape = _obtain_input_shape(input_shape, default_size=299, min_size=139, data_format=K.image_data_format(), require_flatten=False, weights=weights)
    if (input_tensor is None):
        img_input = Input(shape=input_shape)
    elif (not K.is_keras_tensor(input_tensor)):
        img_input = Input(tensor=input_tensor, shape=input_shape)
    else:
        img_input = input_tensor
    if (K.image_data_format() == 'channels_first'):
        channel_axis = 1
    else:
        channel_axis = 3
    x = conv2d_bn(img_input, 32, 3, 3, strides=(2, 2), padding='same')
    x = conv2d_bn(x, 32, 3, 3, padding='same')
    x = conv2d_bn(x, 64, 3, 3)
    x = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    x = conv2d_bn(x, 80, 1, 1, padding='same')
    x = conv2d_bn(x, 192, 3, 3, padding='same')
    x = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)
    branch3x3dbl = conv2d_bn(x, 64, 1, 1)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 32, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3dbl, branch_pool], axis=channel_axis, name='mixed0')
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)
    branch3x3dbl = conv2d_bn(x, 64, 1, 1)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 64, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3dbl, branch_pool], axis=channel_axis, name='mixed1')
    branch1x1 = conv2d_bn(x, 64, 1, 1)
    branch5x5 = conv2d_bn(x, 48, 1, 1)
    branch5x5 = conv2d_bn(branch5x5, 64, 5, 5)
    branch3x3dbl = conv2d_bn(x, 64, 1, 1)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 64, 1, 1)
    x = layers.concatenate([branch1x1, branch5x5, branch3x3dbl, branch_pool], axis=channel_axis, name='mixed2')
    branch3x3 = conv2d_bn(x, 384, 3, 3, strides=(2, 2), padding='same')
    branch3x3dbl = conv2d_bn(x, 64, 1, 1)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3)
    branch3x3dbl = conv2d_bn(branch3x3dbl, 96, 3, 3, strides=(2, 2), padding='same')
    branch_pool = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    x = layers.concatenate([branch3x3, branch3x3dbl, branch_pool], axis=channel_axis, name='mixed3')
    branch1x1 = conv2d_bn(x, 192, 1, 1)
    branch7x7 = conv2d_bn(x, 128, 1, 1)
    branch7x7 = conv2d_bn(branch7x7, 128, 1, 7)
    branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)
    branch7x7dbl = conv2d_bn(x, 128, 1, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 128, 7, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 128, 1, 7)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 128, 7, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 1, 7)
    branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 192, 1, 1)
    x = layers.concatenate([branch1x1, branch7x7, branch7x7dbl, branch_pool], axis=channel_axis, name='mixed4')
    for i in range(2):
        branch1x1 = conv2d_bn(x, 192, 1, 1)
        branch7x7 = conv2d_bn(x, 160, 1, 1)
        branch7x7 = conv2d_bn(branch7x7, 160, 1, 7)
        branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)
        branch7x7dbl = conv2d_bn(x, 160, 1, 1)
        branch7x7dbl = conv2d_bn(branch7x7dbl, 160, 7, 1)
        branch7x7dbl = conv2d_bn(branch7x7dbl, 160, 1, 7)
        branch7x7dbl = conv2d_bn(branch7x7dbl, 160, 7, 1)
        branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 1, 7)
        branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 192, 1, 1)
        x = layers.concatenate([branch1x1, branch7x7, branch7x7dbl, branch_pool], axis=channel_axis, name=('mixed' + str((5 + i))))
    branch1x1 = conv2d_bn(x, 192, 1, 1)
    branch7x7 = conv2d_bn(x, 192, 1, 1)
    branch7x7 = conv2d_bn(branch7x7, 192, 1, 7)
    branch7x7 = conv2d_bn(branch7x7, 192, 7, 1)
    branch7x7dbl = conv2d_bn(x, 192, 1, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 7, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 1, 7)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 7, 1)
    branch7x7dbl = conv2d_bn(branch7x7dbl, 192, 1, 7)
    branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 192, 1, 1)
    x = layers.concatenate([branch1x1, branch7x7, branch7x7dbl, branch_pool], axis=channel_axis, name='mixed7')
    branch3x3 = conv2d_bn(x, 192, 1, 1)
    branch3x3 = conv2d_bn(branch3x3, 320, 3, 3, strides=(2, 2), padding='same')
    branch7x7x3 = conv2d_bn(x, 192, 1, 1)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 1, 7)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 7, 1)
    branch7x7x3 = conv2d_bn(branch7x7x3, 192, 3, 3, strides=(2, 2), padding='same')
    branch_pool = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    x = layers.concatenate([branch3x3, branch7x7x3, branch_pool], axis=channel_axis, name='mixed8')
    for i in range(2):
        branch1x1 = conv2d_bn(x, 320, 1, 1)
        branch3x3 = conv2d_bn(x, 384, 1, 1)
        branch3x3_1 = conv2d_bn(branch3x3, 384, 1, 3)
        branch3x3_2 = conv2d_bn(branch3x3, 384, 3, 1)
        branch3x3 = layers.concatenate([branch3x3_1, branch3x3_2], axis=channel_axis, name=('mixed9_' + str(i)))
        branch3x3dbl = conv2d_bn(x, 448, 1, 1)
        branch3x3dbl = conv2d_bn(branch3x3dbl, 384, 3, 3)
        branch3x3dbl_1 = conv2d_bn(branch3x3dbl, 384, 1, 3)
        branch3x3dbl_2 = conv2d_bn(branch3x3dbl, 384, 3, 1)
        branch3x3dbl = layers.concatenate([branch3x3dbl_1, branch3x3dbl_2], axis=channel_axis)
        branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 192, 1, 1)
        x = layers.concatenate([branch1x1, branch3x3, branch3x3dbl, branch_pool], axis=channel_axis, name=('mixed' + str((9 + i))))
    if include_top:
        x = GlobalAveragePooling2D(name='avg_pool')(x)
        x = Dense(classes, activation='softmax', name='predictions')(x)
    elif (pooling == 'avg'):
        x = GlobalAveragePooling2D()(x)
    elif (pooling == 'max'):
        x = GlobalMaxPooling2D()(x)
    if (input_tensor is not None):
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    model = Model(inputs, x, name='inception_v3')
    if (weights == 'imagenet'):
        if (K.image_data_format() == 'channels_first'):
            if (K.backend() == 'tensorflow'):
                warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
        if include_top:
            weights_path = get_file('inception_v3_weights_tf_dim_ordering_tf_kernels.h5', WEIGHTS_PATH, cache_subdir='models', file_hash='9a0d58056eeedaa3f26cb7ebd46da564')
        else:
            weights_path = get_file('inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5', WEIGHTS_PATH_NO_TOP, cache_subdir='models', file_hash='bcbd6486424b2319ff4ef7d526e38f63')
        model.load_weights(weights_path)
    elif (weights is not None):
        model.load_weights(weights)
    return model
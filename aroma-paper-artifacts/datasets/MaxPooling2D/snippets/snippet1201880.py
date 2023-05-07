from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import warnings
from keras.models import Model
from keras.layers import Activation
from keras.layers import AveragePooling2D
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import Concatenate
from keras.layers import Dense
from keras.layers import GlobalAveragePooling2D
from keras.layers import GlobalMaxPooling2D
from keras.layers import Input
from keras.layers import Lambda
from keras.layers import MaxPooling2D
from keras.utils.data_utils import get_file
from keras.engine.topology import get_source_inputs
from keras.applications import imagenet_utils
from keras import backend as K
import keras
from distutils.version import StrictVersion
from keras.applications.imagenet_utils import _obtain_input_shape
from keras_applications.imagenet_utils import _obtain_input_shape


def InceptionResNetV2(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000):
    'Instantiates the Inception-ResNet v2 architecture.\n    Optionally loads weights pre-trained on ImageNet.\n    Note that when using TensorFlow, for best performance you should\n    set `"image_data_format": "channels_last"` in your Keras config\n    at `~/.keras/keras.json`.\n    The model and the weights are compatible with TensorFlow, Theano and\n    CNTK backends. The data format convention used by the model is\n    the one specified in your Keras config file.\n    Note that the default input image size for this model is 299x299, instead\n    of 224x224 as in the VGG16 and ResNet models. Also, the input preprocessing\n    function is different (i.e., do not use `imagenet_utils.preprocess_input()`\n    with this model. Use `preprocess_input()` defined in this module instead).\n    # Arguments\n        include_top: whether to include the fully-connected\n            layer at the top of the network.\n        weights: one of `None` (random initialization),\n              \'imagenet\' (pre-training on ImageNet),\n              or the path to the weights file to be loaded.\n        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)\n            to use as image input for the model.\n        input_shape: optional shape tuple, only to be specified\n            if `include_top` is `False` (otherwise the input shape\n            has to be `(299, 299, 3)` (with `\'channels_last\'` data format)\n            or `(3, 299, 299)` (with `\'channels_first\'` data format).\n            It should have exactly 3 inputs channels,\n            and width and height should be no smaller than 139.\n            E.g. `(150, 150, 3)` would be one valid value.\n        pooling: Optional pooling mode for feature extraction\n            when `include_top` is `False`.\n            - `None` means that the output of the model will be\n                the 4D tensor output of the last convolutional layer.\n            - `\'avg\'` means that global average pooling\n                will be applied to the output of the\n                last convolutional layer, and thus\n                the output of the model will be a 2D tensor.\n            - `\'max\'` means that global max pooling will be applied.\n        classes: optional number of classes to classify images\n            into, only to be specified if `include_top` is `True`, and\n            if no `weights` argument is specified.\n    # Returns\n        A Keras `Model` instance.\n    # Raises\n        ValueError: in case of invalid argument for `weights`,\n            or invalid input shape.\n    '
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
    x = conv2d_bn(img_input, 32, 3, strides=2, padding='same')
    x = conv2d_bn(x, 32, 3, padding='same')
    x = conv2d_bn(x, 64, 3)
    x = MaxPooling2D(3, strides=2, padding='same')(x)
    x = conv2d_bn(x, 80, 1, padding='same')
    x = conv2d_bn(x, 192, 3, padding='same')
    x = MaxPooling2D(3, strides=2, padding='same')(x)
    branch_0 = conv2d_bn(x, 96, 1)
    branch_1 = conv2d_bn(x, 48, 1)
    branch_1 = conv2d_bn(branch_1, 64, 5)
    branch_2 = conv2d_bn(x, 64, 1)
    branch_2 = conv2d_bn(branch_2, 96, 3)
    branch_2 = conv2d_bn(branch_2, 96, 3)
    branch_pool = AveragePooling2D(3, strides=1, padding='same')(x)
    branch_pool = conv2d_bn(branch_pool, 64, 1)
    branches = [branch_0, branch_1, branch_2, branch_pool]
    channel_axis = (1 if (K.image_data_format() == 'channels_first') else 3)
    x = Concatenate(axis=channel_axis, name='mixed_5b')(branches)
    for block_idx in range(1, 11):
        x = inception_resnet_block(x, scale=0.17, block_type='block35', block_idx=block_idx)
    branch_0 = conv2d_bn(x, 384, 3, strides=2, padding='same')
    branch_1 = conv2d_bn(x, 256, 1)
    branch_1 = conv2d_bn(branch_1, 256, 3)
    branch_1 = conv2d_bn(branch_1, 384, 3, strides=2, padding='same')
    branch_pool = MaxPooling2D(3, strides=2, padding='same')(x)
    branches = [branch_0, branch_1, branch_pool]
    x = Concatenate(axis=channel_axis, name='mixed_6a')(branches)
    for block_idx in range(1, 21):
        x = inception_resnet_block(x, scale=0.1, block_type='block17', block_idx=block_idx)
    branch_0 = conv2d_bn(x, 256, 1)
    branch_0 = conv2d_bn(branch_0, 384, 3, strides=2, padding='same')
    branch_1 = conv2d_bn(x, 256, 1)
    branch_1 = conv2d_bn(branch_1, 288, 3, strides=2, padding='same')
    branch_2 = conv2d_bn(x, 256, 1)
    branch_2 = conv2d_bn(branch_2, 288, 3)
    branch_2 = conv2d_bn(branch_2, 320, 3, strides=2, padding='same')
    branch_pool = MaxPooling2D(3, strides=2, padding='same')(x)
    branches = [branch_0, branch_1, branch_2, branch_pool]
    x = Concatenate(axis=channel_axis, name='mixed_7a')(branches)
    for block_idx in range(1, 10):
        x = inception_resnet_block(x, scale=0.2, block_type='block8', block_idx=block_idx)
    x = inception_resnet_block(x, scale=1.0, activation=None, block_type='block8', block_idx=10)
    x = conv2d_bn(x, 1536, 1, name='conv_7b')
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
    model = Model(inputs, x, name='inception_resnet_v2')
    if (weights == 'imagenet'):
        if (K.image_data_format() == 'channels_first'):
            if (K.backend() == 'tensorflow'):
                warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
        if include_top:
            fname = 'inception_resnet_v2_weights_tf_dim_ordering_tf_kernels.h5'
            weights_path = get_file(fname, (BASE_WEIGHT_URL + fname), cache_subdir='/wdata/backbones_weights', file_hash='e693bd0210a403b3192acc6073ad2e96')
        else:
            fname = 'inception_resnet_v2_weights_tf_dim_ordering_tf_kernels_notop.h5'
            weights_path = get_file(fname, (BASE_WEIGHT_URL + fname), cache_subdir='/wdata/backbones_weights', file_hash='d19885ff4a710c122648d3b5c3b684e4')
        model.load_weights(weights_path, skip_mismatch=True)
    elif (weights is not None):
        model.load_weights(weights)
    return model

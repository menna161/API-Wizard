from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add
from keras.layers import Lambda
from keras.layers import Concatenate
from keras.layers import ZeroPadding2D
from .params import get_conv_params
from .params import get_bn_params


def layer(input_tensor):
    conv_params = get_conv_params()
    bn_params = get_bn_params()
    (conv_name, bn_name, relu_name, sc_name) = handle_block_names(stage, block)
    x = Conv2D(filters, (1, 1), name=(conv_name + '1'), **conv_params)(input_tensor)
    x = BatchNormalization(name=(bn_name + '1'), **bn_params)(x)
    x = Activation('relu', name=(relu_name + '1'))(x)
    x = ZeroPadding2D(padding=(1, 1))(x)
    x = GroupConv2D(filters, (3, 3), conv_params, (conv_name + '2'), strides=strides)(x)
    x = BatchNormalization(name=(bn_name + '2'), **bn_params)(x)
    x = Activation('relu', name=(relu_name + '2'))(x)
    x = Conv2D((filters * 2), (1, 1), name=(conv_name + '3'), **conv_params)(x)
    x = BatchNormalization(name=(bn_name + '3'), **bn_params)(x)
    shortcut = Conv2D((filters * 2), (1, 1), name=sc_name, strides=strides, **conv_params)(input_tensor)
    shortcut = BatchNormalization(name=(sc_name + '_bn'), **bn_params)(shortcut)
    x = Add()([x, shortcut])
    x = Activation('relu', name=relu_name)(x)
    return x

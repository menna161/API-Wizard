from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add
from keras.layers import ZeroPadding2D
from .params import get_conv_params
from .params import get_bn_params


def basic_identity_block(filters, stage, block):
    "The identity block is the block that has no conv layer at shortcut.\n    # Arguments\n        kernel_size: default 3, the kernel size of\n            middle conv layer at main path\n        filters: list of integers, the filters of 3 conv layer at main path\n        stage: integer, current stage label, used for generating layer names\n        block: 'a','b'..., current block label, used for generating layer names\n    # Returns\n        Output tensor for the block.\n    "

    def layer(input_tensor):
        conv_params = get_conv_params()
        bn_params = get_bn_params()
        (conv_name, bn_name, relu_name, sc_name) = handle_block_names(stage, block)
        x = BatchNormalization(name=(bn_name + '1'), **bn_params)(input_tensor)
        x = Activation('relu', name=(relu_name + '1'))(x)
        x = ZeroPadding2D(padding=(1, 1))(x)
        x = Conv2D(filters, (3, 3), name=(conv_name + '1'), **conv_params)(x)
        x = BatchNormalization(name=(bn_name + '2'), **bn_params)(x)
        x = Activation('relu', name=(relu_name + '2'))(x)
        x = ZeroPadding2D(padding=(1, 1))(x)
        x = Conv2D(filters, (3, 3), name=(conv_name + '2'), **conv_params)(x)
        x = Add()([x, input_tensor])
        return x
    return layer
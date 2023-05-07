from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add
from keras.layers import Lambda
from keras.layers import Concatenate
from keras.layers import ZeroPadding2D
from .params import get_conv_params
from .params import get_bn_params


def GroupConv2D(filters, kernel_size, conv_params, conv_name, strides=(1, 1), cardinality=32):

    def layer(input_tensor):
        grouped_channels = (int(input_tensor.shape[(- 1)]) // cardinality)
        blocks = []
        for c in range(cardinality):
            x = Lambda((lambda z: z[(:, :, :, (c * grouped_channels):((c + 1) * grouped_channels))]))(input_tensor)
            name = ((conv_name + '_') + str(c))
            x = Conv2D(grouped_channels, kernel_size, strides=strides, name=name, **conv_params)(x)
            blocks.append(x)
        x = Concatenate(axis=(- 1))(blocks)
        return x
    return layer

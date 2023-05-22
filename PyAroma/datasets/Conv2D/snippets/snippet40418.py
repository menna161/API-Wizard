import keras.backend as K
from keras.layers import Conv2DTranspose as Transpose
from keras.layers import UpSampling2D
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add


def UpsampleBlock(filters, upsample_rate, kernel_size, use_batchnorm=False, upsample_layer='upsampling', conv_name='conv', bn_name='bn', relu_name='relu', up_name='up', **kwargs):
    if (upsample_layer == 'upsampling'):
        UpBlock = Conv2DUpsample
    elif (upsample_layer == 'transpose'):
        UpBlock = Conv2DTranspose
    else:
        raise ValueError(f'Not supported up layer type {upsample_layer}')

    def layer(input_tensor):
        x = UpBlock(filters, upsample_rate=upsample_rate, kernel_size=kernel_size, use_bias=(not use_batchnorm), conv_name=conv_name, up_name=up_name, **kwargs)(input_tensor)
        if use_batchnorm:
            x = BatchNormalization(name=bn_name)(x)
        x = Activation('relu', name=relu_name)(x)
        return x
    return layer

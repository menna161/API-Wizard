from keras.layers import Conv2DTranspose
from keras.layers import UpSampling2D
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Concatenate


def layer(input_tensor):
    (conv_name, bn_name, relu_name, up_name) = handle_block_names(stage)
    x = Conv2DTranspose(filters, transpose_kernel_size, strides=upsample_rate, padding='same', name=up_name, use_bias=(not use_batchnorm))(input_tensor)
    if use_batchnorm:
        x = BatchNormalization(name=(bn_name + '1'))(x)
    x = Activation('relu', name=(relu_name + '1'))(x)
    if (skip is not None):
        x = Concatenate()([x, skip])
    x = ConvRelu(filters, kernel_size, use_batchnorm=use_batchnorm, conv_name=(conv_name + '2'), bn_name=(bn_name + '2'), relu_name=(relu_name + '2'))(x)
    return x

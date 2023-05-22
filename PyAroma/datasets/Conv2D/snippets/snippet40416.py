import keras.backend as K
from keras.layers import Conv2DTranspose as Transpose
from keras.layers import UpSampling2D
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add


def Conv2DUpsample(filters, upsample_rate, kernel_size=(3, 3), up_name='up', conv_name='conv', **kwargs):

    def layer(input_tensor):
        x = UpSampling2D(upsample_rate, name=up_name)(input_tensor)
        x = Conv2D(filters, kernel_size, padding='same', name=conv_name, **kwargs)(x)
        return x
    return layer

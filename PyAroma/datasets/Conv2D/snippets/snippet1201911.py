import keras.backend as K
from keras.layers import Conv2DTranspose as Transpose
from keras.layers import UpSampling2D
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add


def Conv2DTranspose(filters, upsample_rate, kernel_size=(4, 4), up_name='up', **kwargs):

    def layer(input_tensor):
        x = Transpose(filters, kernel_size=kernel_size, strides=upsample_rate, padding='same', name=up_name)(input_tensor)
        return x
    return layer

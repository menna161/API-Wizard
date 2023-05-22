from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Convolution2D, AveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras import backend as K


def reduction_B(input):
    if (K.image_dim_ordering() == 'th'):
        channel_axis = 1
    else:
        channel_axis = (- 1)
    r1 = conv_block(input, 192, 1, 1)
    r1 = conv_block(r1, 192, 3, 3, subsample=(2, 2), border_mode='valid')
    r2 = conv_block(input, 256, 1, 1)
    r2 = conv_block(r2, 256, 1, 7)
    r2 = conv_block(r2, 320, 7, 1)
    r2 = conv_block(r2, 320, 3, 3, subsample=(2, 2), border_mode='valid')
    r3 = MaxPooling2D((3, 3), strides=(2, 2), border_mode='valid')(input)
    m = merge([r1, r2, r3], mode='concat', concat_axis=channel_axis)
    return m

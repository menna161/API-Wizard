import os
import numpy as np
import sys
from loss_functions import *
import nibabel as nib
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import *
from keras.callbacks import *
from glob import glob
from keras.callbacks import *


def get_small_unet_no_pool():
    input_layer = Input(shape=x_train.shape[1:])
    c1 = Conv2D(filters=8, kernel_size=(3, 3), activation='relu', padding='same')(input_layer)
    l = Conv2D(filters=8, kernel_size=(2, 2), strides=(2, 2), activation='relu', padding='same')(c1)
    c2 = Conv2D(filters=16, kernel_size=(3, 3), activation='relu', padding='same')(l)
    l = Conv2D(filters=16, kernel_size=(2, 2), strides=(2, 2), activation='relu', padding='same')(c2)
    c3 = Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same')(l)
    l = Conv2D(filters=32, kernel_size=(2, 2), strides=(2, 2), activation='relu', padding='same')(c3)
    c4 = Conv2D(filters=32, kernel_size=(1, 1), activation='relu', padding='same')(l)
    l = concatenate([UpSampling2D(size=(2, 2))(c4), c3], axis=(- 1))
    l = Conv2D(filters=32, kernel_size=(2, 2), activation='relu', padding='same')(l)
    l = concatenate([UpSampling2D(size=(2, 2))(l), c2], axis=(- 1))
    l = Conv2D(filters=24, kernel_size=(2, 2), activation='relu', padding='same')(l)
    l = concatenate([UpSampling2D(size=(2, 2))(l), c1], axis=(- 1))
    l = Conv2D(filters=16, kernel_size=(2, 2), activation='relu', padding='same')(l)
    l = Conv2D(filters=64, kernel_size=(1, 1), activation='relu')(l)
    l = Dropout(0.5)(l)
    output_layer = Conv2D(filters=1, kernel_size=(1, 1), activation='sigmoid')(l)
    model = Model(input_layer, output_layer)
    return model

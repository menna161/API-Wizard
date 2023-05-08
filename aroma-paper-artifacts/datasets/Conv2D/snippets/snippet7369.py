import os
from tensorflow.keras.layers import Dropout, Concatenate, BatchNormalization
from tensorflow.keras.layers import LeakyReLU, Conv2DTranspose, ZeroPadding2D
from tensorflow.keras.layers import Dense, Reshape, Flatten
from tensorflow.keras.layers import Conv2D, ReLU, Input
from tensorflow.keras import Model
from ..datasets.load_pix2pix_datasets import pix2pix_dataloader
from ..losses.pix2pix_loss import pix2pix_generator_loss, pix2pix_discriminator_loss
import imageio
import cv2
import tensorflow as tf
import numpy as np
import datetime
from tqdm.auto import tqdm


def _downsample(self, filters, kernel_size, kernel_initializer, batchnorm=True):
    model = tf.keras.Sequential()
    model.add(Conv2D(filters, kernel_size=kernel_size, strides=2, kernel_initializer=kernel_initializer, padding='same', use_bias=False))
    if batchnorm:
        model.add(BatchNormalization())
    model.add(LeakyReLU())
    return model

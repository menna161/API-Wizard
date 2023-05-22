import cv2
import os
from tensorflow.keras.layers import Dropout, BatchNormalization, Lambda
from tensorflow.keras.layers import Dense, Reshape, Input, ReLU, Conv2D
from tensorflow.keras.layers import Conv2DTranspose, Embedding, Flatten
from tensorflow.keras import Model
import imageio
import numpy as np
from ..datasets.load_custom_data import load_custom_data_AE
from ..datasets.load_mnist import load_mnist_AE
from ..datasets.load_cifar10 import load_cifar10_AE
import datetime
from ..losses.mse_loss import mse_loss
import tensorflow as tf
from tqdm.auto import tqdm


def __init__(self, config, image_size):
    super(decoder, self).__init__()
    self.num_hiddens = config['num_hiddens']
    self.num_residual_hiddens = config['num_residual_hiddens']
    self.num_residual_layers = config['num_residual_layers']
    self.conv1 = Conv2D(self.num_hiddens, kernel_size=(3, 3), strides=(1, 1), padding='same')
    self.residual_stack = residual(self.num_hiddens, self.num_residual_layers, self.num_residual_hiddens)
    self.flatten = Flatten()
    self.dense1 = Dense((((image_size[0] // 4) * (image_size[1] // 4)) * 128), activation='relu')
    self.reshape = Reshape(((image_size[0] // 4), (image_size[1] // 4), 128))
    self.upconv1 = Conv2DTranspose((self.num_hiddens // 2), kernel_size=(4, 4), strides=(2, 2), activation='relu', padding='same')
    self.upconv2 = Conv2DTranspose(image_size[(- 1)], kernel_size=(4, 4), strides=(2, 2), padding='same')

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
    super(nn_model, self).__init__()
    embedding_dim = config['embedding_dim']
    commiment_cost = config['commiment_cost']
    num_embeddings = config['num_embeddings']
    self.encoder = encoder(config)
    self.pre_vq_conv = Conv2D(embedding_dim, kernel_size=(1, 1), strides=(1, 1))
    self.decoder = decoder(config, image_size)
    self.vq_vae = VectorQuantizer(num_embeddings, embedding_dim, commiment_cost)

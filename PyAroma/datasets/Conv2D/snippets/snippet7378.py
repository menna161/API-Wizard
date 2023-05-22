from ..layers import SpectralNormalization, GenResBlock, SelfAttention, DiscResBlock, DiscOptResBlock
import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_cifar10 import load_cifar10_with_labels
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.hinge_loss import hinge_loss_generator, hinge_loss_discriminator
import datetime
from tqdm import tqdm
import logging
import imageio


def __init__(self, n_classes, filters=64):
    super(Generator, self).__init__()
    self.filters = filters
    self.sn_linear = SpectralNormalization(tf.keras.layers.Dense((((filters * 16) * 4) * 4)))
    self.rs = tf.keras.layers.Reshape((4, 4, (16 * filters)))
    self.res_block1 = GenResBlock(n_classes=n_classes, filters=(filters * 16), spectral_norm=True)
    self.res_block2 = GenResBlock(n_classes=n_classes, filters=(filters * 8), spectral_norm=True)
    self.res_block3 = GenResBlock(n_classes=n_classes, filters=(filters * 4), spectral_norm=True)
    self.attn = SelfAttention(spectral_norm=True)
    self.res_block4 = GenResBlock(n_classes=n_classes, filters=(filters * 2), spectral_norm=True)
    self.res_block5 = GenResBlock(n_classes=n_classes, filters=filters, spectral_norm=True)
    self.bn1 = tf.keras.layers.BatchNormalization()
    self.snconv2d1 = SpectralNormalization(tf.keras.layers.Conv2D(kernel_size=3, filters=3, strides=1, padding='same'))

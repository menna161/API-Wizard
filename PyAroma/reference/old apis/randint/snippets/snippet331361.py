from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import LearningRateScheduler
from keras.layers import Activation
from keras import backend as K
from keras.models import Model
from models.wide_residual_network import create_wide_residual_network, SGDTorch, dense
from utils import load_cifar10, normalize_minus1_1, save_roc_pr_curve_data
from transformations import Transformer


def data_gen(x, y, batch_size):
    while True:
        ind_permutation = np.random.permutation(len(x))
        for b_start_ind in range(0, len(x), batch_size):
            batch_inds = ind_permutation[b_start_ind:(b_start_ind + batch_size)]
            x_batch = x[batch_inds]
            y_batch = y[batch_inds].flatten()
            if (K.image_data_format() == 'channels_first'):
                x_batch = np.transpose(x_batch, (0, 2, 3, 1))
            y_t_batch = np.random.randint(0, transformer.n_transforms, size=len(x_batch))
            x_batch = transformer.transform_batch(x_batch, y_t_batch)
            if (K.image_data_format() == 'channels_first'):
                x_batch = np.transpose(x_batch, (0, 3, 1, 2))
            (yield (x_batch, [to_categorical(y_batch, num_classes=10), to_categorical(y_t_batch, num_classes=transformer.n_transforms)]))

import os
from tensorflow.keras.layers import Conv2D, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.layers import Conv2DTranspose, Dense, Reshape, Flatten
from tensorflow.keras import Model
from ..datasets.load_cifar10 import load_cifar10
from ..datasets.load_mnist import load_mnist
from ..datasets.load_custom_data import load_custom_data
from ..datasets.load_cifar100 import load_cifar100
from ..datasets.load_lsun import load_lsun
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
import cv2
import numpy as np
import datetime
import tensorflow as tf
import imageio
from tqdm.auto import tqdm


def generate_samples(self, n_samples=1, save_dir=None):
    'Generate samples using the trained model\n\n        Args:\n            n_samples (int, optional): number of samples to generate. Defaults to ``1``\n            save_dir (str, optional): directory to save the generated images. Defaults to ``None``\n\n        Return:\n            returns ``None`` if save_dir is ``not None``, otherwise returns a numpy array with generated samples\n        '
    if (self.gen_model is None):
        self.__load_model()
    Z = tf.random.normal([n_samples, self.noise_dim])
    generated_samples = self.gen_model(Z).numpy()
    if (save_dir is None):
        return generated_samples
    assert os.path.exists(save_dir), 'Directory does not exist'
    for (i, sample) in enumerate(generated_samples):
        imageio.imwrite(os.path.join(save_dir, (('sample_' + str(i)) + '.jpg')), sample)

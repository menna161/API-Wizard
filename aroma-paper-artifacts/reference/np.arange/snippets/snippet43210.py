from keras.datasets import cifar10
import numpy as np


def shuffle_samples(self):
    image_indices = np.random.permutation(np.arange(self.num_samples))
    self.images = self.images[image_indices]

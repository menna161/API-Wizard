import matplotlib.pylab as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import keras
from keras.models import Sequential
from keras.layers import Conv2D


def show_cat(cat_batch):
    print('cat shape before transfo', cat_batch.shape)
    cat = np.squeeze(cat_batch, axis=0)
    print('cat.shape', cat.shape)
    plt.imshow(cat)
    plt.show()

import matplotlib.pylab as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import keras
from scipy import misc
from keras.models import Sequential
from keras.layers import Conv2D


def resize_cat(cat):
    cat = scipy.misc.imresize(cat, size=((cat.shape[0] / 2), (cat.shape[1] / 2)))
    plt.imshow(cat)
    plt.show()

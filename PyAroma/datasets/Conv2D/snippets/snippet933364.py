import numpy as np
import keras
import gym
import os
import h5py
import matplotlib
import scipy
from matplotlib import pyplot as plt
from scipy import misc
from keras.models import Sequential
from keras.layers import Conv2D
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers


def preprocessing(I):
    ' prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector '
    I = I[35:195]
    I = I[(::2, ::2, 0)]
    I = scipy.misc.imresize(I, size=(img_dim, img_dim))
    I[(I == 144)] = 0
    I[(I == 109)] = 0
    I = (I / 255)
    return I.astype(np.float).ravel()

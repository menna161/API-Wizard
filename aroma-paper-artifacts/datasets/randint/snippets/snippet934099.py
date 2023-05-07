import numpy as np
import keras
import gym
import pygal
import os
import h5py
import math
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers


def add_controlled_noise(targetModel, big_sigma, largeNoise=False):
    tR = memoryR
    tX = memoryS
    tY = memoryA
    tW = memoryW
    train_C = np.random.randint(tY.shape[0], size=100)
    tX = tX[(train_C, :)]
    tY_old = tY[(train_C, :)]
    tY_new = tY[(train_C, :)]
    diffs = np.zeros(np.alen(tX))
    delta = 1000
    deltaCount = 0
    while (((delta > 3) or (delta < 0.1)) and (deltaCount < 20)):
        targetModel = add_noise_to_model(targetModel, largeNoise)
        for i in range(np.alen(tX)):
            a = GetRememberedOptimalPolicy(tX[i])
            b = GetRememberedOptimalPolicyFromNoisyModel(targetModel, tX[i])
            a = a.flatten()
            b = b.flatten()
            c = np.abs((a - b))
            diffs[i] = c.mean()
        delta = np.average(diffs)
        deltaCount += 1
        if ((delta > 3) or (delta < 0.1)):
            print('Delta', delta, ' out of bound adjusting big_sigma', big_sigma, 'to', (1 / delta))
            big_sigma = (1 / delta)
    print('Tried x time ', deltaCount, 'delta =', delta)
    return (targetModel, big_sigma)

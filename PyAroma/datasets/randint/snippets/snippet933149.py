import numpy as np
import keras
import gym
import pybullet
import pybullet_envs
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


def add_controlled_noise(largeNoise=False):
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
    while (delta > 1):
        add_noise_to_model(True)
        for i in range(np.alen(tX)):
            a = GetRememberedOptimalPolicy(tX[i])
            b = GetRememberedOptimalPolicyFromNoisyModel(tX[i])
            a = a.flatten()
            b = b.flatten()
            c = np.abs((a - b))
            diffs[i] = c.mean()
        delta = np.average(diffs)
        deltaCount += 1
    print('Tried x time ', deltaCount, 'delta =', delta)

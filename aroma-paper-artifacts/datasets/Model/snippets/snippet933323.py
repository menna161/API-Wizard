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
    for i in range(np.alen(tX)):
        a = GetRememberedOptimalPolicyFromNoisyModel(noisy_model, tX[i])
        a = a.flatten()
    while (((delta > upper_delta) or (delta < lower_delta)) and (deltaCount < 3)):
        reset_noisy_model()
        targetModel = noisy_model
        targetModel = add_noise_to_model(noisy_model, largeNoise)
        for i in range(np.alen(tX)):
            b = GetRememberedOptimalPolicyFromNoisyModel(targetModel, tX[i])
            b = b.flatten()
        c = np.abs((a - b))
        delta = c.mean()
        deltaCount += 1
        if (delta > upper_delta):
            big_sigma = (big_sigma * 0.9)
        if (delta < lower_delta):
            big_sigma = (big_sigma * 1.1)
    print('Tried x time ', deltaCount, 'delta =', delta, 'big_sigma ', big_sigma)
    return (targetModel, big_sigma)

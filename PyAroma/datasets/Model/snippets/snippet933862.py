import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from keras import optimizers


def add_controlled_noise(targetModel, largeNoise=False):
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
    while ((delta > 6) and (deltaCount < 20)):
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
    print('Tried x time ', deltaCount, 'delta =', delta)
    return targetModel

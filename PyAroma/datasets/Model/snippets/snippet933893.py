import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
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
    while (((delta > upper_delta) or (delta < lower_delta)) and (deltaCount < 5)):
        add_noise_TF(largeNoise)
        for i in range(np.alen(tX)):
            a = GetRememberedOptimalPolicy(tX[i])
            b = GetRememberedOptimalPolicyFromNoisyModel(tX[i])
            a = a.flatten()
            b = b.flatten()
            c = np.abs((a - b))
            diffs[i] = c.mean()
        delta = np.average(diffs)
        deltaCount += 1
        if (delta > upper_delta):
            big_sigma = (big_sigma * 0.9)
            print('Delta', delta, ' out of bound adjusting big_sigma', big_sigma)
        if (delta < lower_delta):
            big_sigma = (big_sigma * 1.1)
            print('Delta', delta, ' out of bound adjusting big_sigma', big_sigma)
    print('Tried x time ', deltaCount, 'delta =', delta)
    return big_sigma

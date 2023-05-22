import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from random import gauss


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
        a = GetRememberedOptimalPolicyFromNoisyModel(tX[i])
        a = a.flatten()
    while (((delta > upper_delta) or (delta < lower_delta)) and (deltaCount < 1)):
        reset_noisy_model_TF()
        targetModel
        add_noise_TF(largeNoise)
        for i in range(np.alen(tX)):
            b = GetRememberedOptimalPolicyFromNoisyModel(tX[i])
            b = b.flatten()
        c = np.abs((a - b))
        delta = c.mean()
        deltaCount += 1
        if USES_ADAPTIVE_NOISE:
            if (delta > upper_delta):
                big_sigma = (big_sigma * 0.9)
                print('Delta', delta, ' out of bound adjusting big_sigma', big_sigma)
            if (delta < lower_delta):
                big_sigma = (big_sigma * 1.1)
                print('Delta', delta, ' out of bound adjusting big_sigma', big_sigma)
    print('Tried x time ', deltaCount, 'delta =', delta)
    return big_sigma

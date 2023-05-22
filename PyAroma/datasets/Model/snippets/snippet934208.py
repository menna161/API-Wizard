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


def pr_noisy_actor_experience_replay(memSA, memR, memS, memA, memW, num_epochs=1):
    tSA = memSA
    tR = memR
    tX = memS
    tY = memA
    tW = memW
    tX_train = np.zeros(shape=(1, num_env_variables))
    tY_train = np.zeros(shape=(1, num_env_actions))
    for i in range(np.alen(tR)):
        pr = predictTotalRewards(tX[i], GetRememberedOptimalPolicyFromNoisyModel(noisy_model, tX[i]))
        d = math.fabs((memoryR.max() - pr))
        tW[i] = 5e-16
        if (tR[i] > pr):
            tW[i] = 0.85
        if (tR[i] > (pr + (d / 2))):
            tW[i] = 1
        if (tW[i] > np.random.rand(1)):
            tX_train = np.vstack((tX_train, tX[i]))
            tY_train = np.vstack((tY_train, tY[i]))
    tX_train = tX_train[1:]
    tY_train = tY_train[1:]
    print(('%8d were better After removing first element' % np.alen(tX_train)))
    if (np.alen(tX_train) > 0):
        noisy_model.fit(tX_train, tY_train, batch_size=mini_batch, nb_epoch=num_epochs, verbose=0)

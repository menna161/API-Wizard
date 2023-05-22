import numpy as np
import keras
import gym
import pygal
import os
import h5py
import math
from random import gauss
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers
import keras.backend as K


def pr_actor_experience_replay(memSA, memR, memS, memA, memW, num_epochs=1):
    for t in range(training_epochs):
        tSA = (memSA + 0.0)
        tR = (memR + 0.0)
        tX = (memS + 0.0)
        tY = (memA + 0.0)
        tW = (memW + 0.0)
        tS = (memW + 0.0)
        treshold = memoryR.mean()
        gameAverage = memoryR.mean()
        gameDistance = math.fabs((memoryW.max() - memoryR.mean()))
        gameTreshold = (memoryW.mean() + (gameDistance * 0.4))
        train_C = np.arange(np.alen(tR))
        train_C = train_C[(tR.flatten() > treshold)]
        tX = tX[(train_C, :)]
        tY = tY[(train_C, :)]
        tW = tW[(train_C, :)]
        tR = tR[(train_C, :)]
        tS = tS[(train_C, :)]
        train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tR))))
        tX = tX[(train_A, :)]
        tY = tY[(train_A, :)]
        tW = tW[(train_A, :)]
        tR = tR[(train_A, :)]
        tS = tS[(train_A, :)]
        tX_train = np.zeros(shape=(1, num_env_variables))
        tY_train = np.zeros(shape=(1, num_env_actions))
        for i in range(np.alen(tR)):
            pr = predictTotalRewards(tX[i], GetRememberedOptimalPolicy(tX[i]))
            d = math.fabs((memoryR.max() - pr))
            tW[i] = 5e-16
            if (tR[i] > pr):
                tW[i] = 0.15
            if (tR[i] > (pr + (d * 0.0))):
                tW[i] = 1
            if (tW[i] > np.random.rand(1)):
                tX_train = np.vstack((tX_train, tX[i]))
                tY_train = np.vstack((tY_train, tY[i]))
        tX_train = tX_train[1:]
        tY_train = tY_train[1:]
        print(('%8d were better After removing first element' % np.alen(tX_train)))
        if (np.alen(tX_train) > 0):
            action_predictor_model.fit(tX_train, tY_train, batch_size=mini_batch, nb_epoch=1, verbose=0)

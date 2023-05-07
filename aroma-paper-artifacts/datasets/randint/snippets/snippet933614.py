import numpy as np
import keras
import gym
import roboschool
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


def actor_experience_replay(memSA, memR, memS, memA, memW, num_epochs=1):
    for t in range(training_epochs):
        tSA = (memSA + 0.0)
        tR = (memR + 0.0)
        tX = (memS + 0.0)
        tY = (memA + 0.0)
        tW = (memW + 0.0)
        tS = (memW + 0.0)
        stdDev = np.std(tR)
        gameStdDev = np.std(tS)
        distance = math.fabs((memoryR.max() - memoryR.mean()))
        treshold = (memoryR.mean() + (stdDev * 1))
        gameAverage = memoryR.mean()
        gameDistance = math.fabs((memoryW.max() - memoryR.mean()))
        gameTreshold = (memoryW.mean() + (gameStdDev * 0))
        train_C = np.arange(np.alen(tR))
        tX = tX[(train_C, :)]
        tY = tY[(train_C, :)]
        tW = tW[(train_C, :)]
        tR = tR[(train_C, :)]
        tS = tS[(train_C, :)]
        if (np.alen(tR) <= 0):
            break
        train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tR))))
        tX = tX[(train_A, :)]
        tY = tY[(train_A, :)]
        tW = tW[(train_A, :)]
        tR = tR[(train_A, :)]
        tS = tS[(train_A, :)]
        train_D = np.arange(np.alen(tR))
        train_D = train_D[(tR.flatten() > treshold)]
        tX = tX[(train_D, :)]
        tY = tY[(train_D, :)]
        tW = tW[(train_D, :)]
        tR = tR[(train_D, :)]
        tS = tS[(train_D, :)]
        tX_train = tX
        tY_train = tY
        if ((t % 89) == 1):
            print(('%8d were better After removing first element' % np.alen(tX_train)), 'Upper_cut', (memoryR.mean() + stdDev), 'gameStdDev', (memoryW.mean() + gameStdDev))
        if (np.alen(tX_train) > 0):
            action_predictor_model.fit(tX_train, tY_train, batch_size=mini_batch, nb_epoch=1, verbose=0)

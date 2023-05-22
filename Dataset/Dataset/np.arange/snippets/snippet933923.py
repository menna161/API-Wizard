import tensorflow as tf
import numpy as np
import gym
import pybullet
import pybullet_envs
import pygal
import os
import h5py
import math
from keras import optimizers


def actor_experience_replay(memSA, memR, memS, memA, memW, num_epoch=1):
    tSA = memSA
    tR = memR
    tX = memS
    tY = memA
    tW = memW
    target = tR.mean()
    train_C = np.arange(np.alen(tR))
    train_C = train_C[(tR.flatten() > target)]
    tX = tX[(train_C, :)]
    tY = tY[(train_C, :)]
    tW = tW[(train_C, :)]
    tR = tR[(train_C, :)]
    train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tR))))
    tX = tX[(train_A, :)]
    tY = tY[(train_A, :)]
    tW = tW[(train_A, :)]
    tR = tR[(train_A, :)]
    train_B = np.arange(np.alen(tR))
    tX_train = np.zeros(shape=(1, num_env_variables))
    tY_train = np.zeros(shape=(1, num_env_actions))
    for i in range(np.alen(train_B)):
        ' YOU CAN"T USE predictTotalRewards\n        IF YOU DON"T TRAIN THE QMODEL\n\n        if tR[i][0] < pr:\n            tW[i][0] = -1\n        else:\n        '
        d = math.fabs((memoryR.max() - target))
        tW[i] = (math.fabs((tR[i] - (target + 5e-12))) / d)
        tW[i] = 5e-16
        if (tR[i] > target):
            tW[i] = 0.5
        if (tR[i] > max_game_average):
            tW[i] = 1
        if (tW[i] > np.random.rand(1)):
            tX_train = np.vstack((tX_train, tX[i]))
            tY_train = np.vstack((tY_train, tY[i]))
    '\n    train_B = train_B[tW.flatten()>0]\n\n    #print("%8d were better results than pr"%np.alen(tX_train))\n\n    tX = tX[train_B,:]\n    tY = tY[train_B,:]\n    tW = tW[train_B,:]\n    tR = tR[train_B,:]\n    #print("tW",tW)\n    '
    ' REMOVE FIRST ELEMENT BEFORE TRAINING '
    tX_train = tX_train[1:]
    tY_train = tY_train[1:]
    if (np.alen(tX_train) > 0):
        for num_epoch in range(training_epochs):
            sess.run(aptrain_op, feed_dict={apdataX: tX_train, apdataY: tY_train})

from environments.rocketlander import RocketLander
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


def pr_actor_experience_replay(memSA, memR, memS, memA, memW, num_epoch=1):
    for num_epoch in range(training_epochs):
        tSA = (memSA + 0.0)
        tR = (memR + 0.0)
        tX = (memS + 0.0)
        tY = (memA + 0.0)
        tW = (memW + 0.0)
        tS = (memW + 0.0)
        game_max = (tW.max() + 0.0)
        gameAverage = memR.mean()
        treshold = memR.flatten()[(- 5000):].mean()
        train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tR))))
        tSA = tSA[(train_A, :)]
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
            if ((tR[i] > pr) and (tS[i] > gameAverage)):
                tW[i] = 0.005
            if ((tR[i] > pr) and (tS[i] > treshold)):
                tW[i] = 0.55
            if ((tR[i] > (pr + (d * 0.005))) and (tR[i] > game_max)):
                tW[i] = 1
            if (tW[i] > np.random.rand(1)):
                tX_train = np.vstack((tX_train, tX[i]))
                tY_train = np.vstack((tY_train, tY[i]))
        tX_train = tX_train[1:]
        tY_train = tY_train[1:]
        print(num_epoch, ('%8d were better After removing first element' % np.alen(tX_train)))
        if (np.alen(tX_train) > 0):
            for t in range(25):
                sess.run(aptrain_op, feed_dict={apdataX: tX_train, apdataY: tY_train})

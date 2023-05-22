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


def GetRememberedOptimalPolicyFromNoisyModel(qstate):
    predX = np.zeros(shape=(1, num_env_variables))
    predX[0] = qstate
    inputVal = predX[0].reshape(1, predX.shape[1])
    pred = sess.run(napy_x, feed_dict={apdataX: inputVal})
    r_remembered_optimal_policy = pred[0]
    return r_remembered_optimal_policy
import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from random import gauss


def GetRememberedOptimalPolicyFromNoisyModel(qstate):
    predX = np.zeros(shape=(1, num_env_variables))
    predX[0] = qstate
    inputVal = predX[0].reshape(1, predX.shape[1])
    pred = sess.run(napy_x, feed_dict={apdataX: inputVal})
    r_remembered_optimal_policy = pred[0]
    return r_remembered_optimal_policy

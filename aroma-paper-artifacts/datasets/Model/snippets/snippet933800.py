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


def GetRememberedOptimalPolicyFromNoisyModel(qstate):
    predX = np.zeros(shape=(1, num_env_variables))
    predX[0] = qstate
    pred = noisy_model.predict(predX[0].reshape(1, predX.shape[1]))
    r_remembered_optimal_policy = pred[0]
    return r_remembered_optimal_policy

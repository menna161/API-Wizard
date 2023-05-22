import numpy as np
import keras
import gym
import pygal
import os
import h5py
import matplotlib.pyplot as plt
import math
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras import optimizers


def train_critic():
    tSA = memorySA
    tR = memoryR
    train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tR))))
    tR = tR[(train_A, :)]
    tSA = tSA[(train_A, :)]
    Qmodel.fit(tSA, tR, batch_size=mini_batch, nb_epoch=training_epochs, verbose=0)

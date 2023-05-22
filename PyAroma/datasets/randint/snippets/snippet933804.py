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


def train_noisy_actor():
    tX = memoryS
    tY = memoryA
    tW = memoryW
    train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tY))))
    tX = tX[(train_A, :)]
    tY = tY[(train_A, :)]
    tW = tW[(train_A, :)]
    noisy_model.fit(tX, tY, batch_size=mini_batch, nb_epoch=training_epochs, verbose=0)

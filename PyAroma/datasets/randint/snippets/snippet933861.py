import tensorflow as tf
import numpy as np
import gym
import pygal
import os
import h5py
import math
from keras import optimizers


def train_noisy_actor():
    tX = memoryS
    tY = memoryA
    tW = memoryW
    train_A = np.random.randint(tY.shape[0], size=int(min(experience_replay_size, np.alen(tY))))
    tX = tX[(train_A, :)]
    tY = tY[(train_A, :)]
    tW = tW[(train_A, :)]
    for num_epoch in range(training_epochs):
        sess.run(natrain_op, feed_dict={apdataX: tX, apdataY: tY})

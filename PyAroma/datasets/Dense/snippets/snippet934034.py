import numpy as np
import keras
import gym
import roboschool
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import optimizers
from Lib.Individual import Individual


def create_model(network_width, network_hidden_layers, observation_space, action_space):
    action_predictor_model = Sequential()
    action_predictor_model.add(Dense(network_width, activation='relu', input_dim=observation_space))
    for i in range(network_hidden_layers):
        action_predictor_model.add(Dense(network_width, activation='relu'))
    action_predictor_model.add(Dense(action_space))
    return action_predictor_model

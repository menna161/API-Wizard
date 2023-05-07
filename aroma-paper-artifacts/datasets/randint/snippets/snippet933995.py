import numpy as np
import keras
import gym
from random import gauss
import roboschool
import math
from random import randint
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import optimizers
from Lib.Individual import Individual


def populate_next_generation(generationID, top_individuals, population_size, network_width, network_hidden_layers, observation_space, action_space, total_population_counter):
    newPop = top_individuals
    num_selected = len(top_individuals)
    for i in range((population_size - len(top_individuals))):
        newModel = create_model(network_width, network_hidden_layers, observation_space, action_space)
        model1 = top_individuals[0].network
        model2 = top_individuals[1].network
        sz = len(newModel.layers)
        for k in range(sz):
            w = newModel.layers[k].get_weights()
            w1 = model1.layers[k].get_weights()
            w2 = model2.layers[k].get_weights()
            if (np.alen(w) > 0):
                for j in range(np.alen(w[0])):
                    y = w[0][j]
                    y1 = w1[0][j]
                    y2 = w2[0][j]
                    for l in range(np.alen(y)):
                        z = y[l]
                        parentID = randint(0, (num_selected - 1))
                        parent = top_individuals[parentID]
                        parentNetwork = parent.network
                        z1 = parentNetwork.layers[k].get_weights()[0][j][l]
                        z = (z1 + 0.0)
                        y[l] = z
                    w[0][j] = y
            newModel.layers[k].set_weights(w)
        top_individuals.append(Individual(generationID, total_population_counter, newModel))
        total_population_counter += 1
    return (top_individuals, total_population_counter)

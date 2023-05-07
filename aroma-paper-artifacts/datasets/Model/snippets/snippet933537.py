import numpy as np
import keras
import gym
from random import gauss
import math
from random import randint
import tensorflow as tf
from Lib.Individual import IndividualTF


def create_individualTF(network_width, network_hidden_layers, observation_space, action_space):
    ' apModel '
    apw_h = init_weights([OBSERVATION_SPACE, 2048])
    apw_h2 = init_weights([32, 32])
    apw_h3 = init_weights([32, 32])
    apw_o = init_weights([2048, ACTION_SPACE])
    appy_x = apModel(apdataX, apw_h, apw_o)
    apcost = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(apdataY, appy_x))))
    apOptimizer = tf.train.AdadeltaOptimizer(1.0, 0.9, 1e-06)
    aptrain_op = apOptimizer.minimize(apcost)
    ' end apModel '
    sess.run(tf.global_variables_initializer())
    indiv = IndividualTF(generationID=generations_count, indivID=total_population_counter, apw_h=apw_h, apw_h2=apw_h2, apw_h3=apw_h3, apw_o=apw_o, appy_x=appy_x)
    print('Creating individual ', generations_count)
    return indiv

import numpy as np
import keras
import gym
from random import gauss
import math
from random import randint
import tensorflow as tf
from Lib.Individual import IndividualTF


def mergeArraysRandom(arr1, arr2):
    a = arr1
    b = arr2
    af = a.flatten()
    bf = b.flatten()
    comb = np.array([af, bf])
    res = np.zeros(np.alen(af))
    for i in range(np.alen(af)):
        res[i] = (comb[(np.random.randint(0, 2), i)] + 0.0)
    fres = res.reshape(a.shape[0], a.shape[1])
    return fres

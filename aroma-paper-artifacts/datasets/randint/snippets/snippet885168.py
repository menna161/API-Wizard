from __future__ import print_function
import random as rand
import csv
import operator
import gc
import os
from datetime import datetime
from keras.callbacks import EarlyStopping
from keras.models import load_model
import keras.backend as K
from sklearn.metrics import log_loss
import numpy as np
import tensorflow as tf


def _crossover(self, genome1, genome2):
    cross_ind = rand.randint(0, len(genome1))
    child = (genome1[:cross_ind] + genome2[cross_ind:])
    return child

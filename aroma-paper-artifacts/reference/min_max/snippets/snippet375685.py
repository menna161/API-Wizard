import logging
import traceback
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ConfigSpace.hyperparameters import CategoricalHyperparameter, UniformFloatHyperparameter, UniformIntegerHyperparameter
from ConfigSpace.conditions import EqualsCondition, InCondition
from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace import Configuration
from aslib_scenario.aslib_scenario import ASlibScenario
from sklearn.utils import check_array
from sklearn.tree._tree import DTYPE


def __init__(self, classifier_class):
    '\n            Constructor\n        '
    self.classifiers = []
    self.logger = logging.getLogger('MultiClassifier')
    self.classifier_class = classifier_class
    self.normalizer = MinMaxScaler()

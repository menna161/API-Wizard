from abc import ABC, abstractmethod
import logging
from typing import Iterable, Sequence
import acton.database
import acton.kde_predictor
import GPy as gpy
import numpy
import sklearn.base
import sklearn.linear_model
import sklearn.model_selection
import sklearn.preprocessing
from numpy.random import multivariate_normal, gamma, multinomial
from scipy.stats import norm


def _linear_regression() -> type:
    return from_class(sklearn.linear_model.LinearRegression, regression=True)

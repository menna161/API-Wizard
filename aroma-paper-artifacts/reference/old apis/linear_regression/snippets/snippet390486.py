from itertools import product
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import matplotlib.pyplot as plt
from basis_expansions import Binner, GaussianKernel, Polynomial, LinearSpline, CubicSpline, NaturalCubicSpline
from dftransformers import ColumnSelector, FeatureUnion, Intercept, MapFeature
from simulation import run_simulation_expreiment, plot_simulation_expreiment, make_random_train_test, run_residual_simulation
from matplotlib import cm


def make_binned_regression(n_cuts):
    return Pipeline([('binner', Binner(0, 1, n_cuts=n_cuts)), ('regression', LinearRegression(fit_intercept=False))])
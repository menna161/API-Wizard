import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import catboost
from catboost import Pool
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from copy import deepcopy
from bartpy.sklearnmodel import SklearnModel
import seaborn as sns
import seaborn as sns
import seaborn as sns


def fit_linear_model(X_train, y_train, X_test, y_test):
    rebased_x = np.sin(X_train[:, 0]).reshape((- 1), 1)
    linear_model = LinearRegression()
    linear_model.fit(rebased_x, y_train)
    pred = linear_model.predict(np.sin(X_test[:, 0]).reshape((- 1), 1))
    score = linear_model.score(np.sin(X_test[:, 0]).reshape((- 1), 1), y_test)
    return (linear_model, pred, score)

import datetime
import math
import os
import random
import sys
import warnings
import dill
import pathos
import numpy as np
import pandas as pd
import scipy
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, brier_score_loss, make_scorer, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from quantile_ml import DataFrameVectorizer
from quantile_ml import utils
from quantile_ml import utils_categorical_ensembling
from quantile_ml import utils_data_cleaning
from quantile_ml import utils_feature_selection
from quantile_ml import utils_model_training
from quantile_ml import utils_models
from quantile_ml import utils_scaling
from quantile_ml import utils_scoring
import xgboost as xgb
from keras.models import Model


def print_results(self, model_name):
    if (self.ml_for_analytics and (model_name in ('LogisticRegression', 'RidgeClassifier', 'LinearRegression', 'Ridge'))):
        self._print_ml_analytics_results_linear_model()
    elif (self.ml_for_analytics and (model_name in ['RandomForestClassifier', 'RandomForestRegressor', 'XGBClassifier', 'XGBRegressor', 'GradientBoostingRegressor', 'GradientBoostingClassifier', 'LGBMRegressor', 'LGBMClassifier'])):
        self._print_ml_analytics_results_random_forest()

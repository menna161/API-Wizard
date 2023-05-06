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


def _get_estimator_names(self):
    if (self.type_of_estimator == 'regressor'):
        base_estimators = ['GradientBoostingRegressor']
        if (self.compare_all_models != True):
            return base_estimators
        else:
            base_estimators.append('RANSACRegressor')
            base_estimators.append('RandomForestRegressor')
            base_estimators.append('LinearRegression')
            base_estimators.append('AdaBoostRegressor')
            base_estimators.append('ExtraTreesRegressor')
            return base_estimators
    elif (self.type_of_estimator == 'classifier'):
        base_estimators = ['GradientBoostingClassifier']
        if (self.compare_all_models != True):
            return base_estimators
        else:
            base_estimators.append('LogisticRegression')
            base_estimators.append('RandomForestClassifier')
            return base_estimators
    else:
        raise 'TypeError: type_of_estimator must be either "classifier" or "regressor".'

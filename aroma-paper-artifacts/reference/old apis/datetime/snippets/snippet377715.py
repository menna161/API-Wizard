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


def fit_single_pipeline(self, X_df, y, model_name, feature_learning=False):
    full_pipeline = self._construct_pipeline(model_name=model_name, feature_learning=feature_learning)
    ppl = full_pipeline.named_steps['final_model']
    if self.verbose:
        print('\n\n********************************************************************************************')
        if (self.name is not None):
            print(self.name)
        print(((('About to fit the pipeline for the model ' + model_name) + ' to predict ') + self.output_column))
        print('Started at:')
        start_time = datetime.datetime.now().replace(microsecond=0)
        print(start_time)
    ppl.fit(X_df, y)
    if self.verbose:
        print('Finished training the pipeline!')
        print('Total training time:')
        print((datetime.datetime.now().replace(microsecond=0) - start_time))
    self.trained_final_model = ppl
    self.print_results(model_name)
    return ppl

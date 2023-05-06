import signal
import numpy as np
import os
import pandas as pd
import sklearn.model_selection
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
from tqdm import tqdm
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from autosklearn.metrics import f1_weighted
from autosklearn.metrics import mean_squared_error
from tpot import TPOTClassifier
from tpot import TPOTRegressor
from ..config import classifier_config_dict
import h2o
from h2o.automl import H2OAutoML
from auto_ml import Predictor


def process_auto_ml(X_train, X_test, y_train, df_types, m_type, seed, *args):
    'Function that trains and tests data using auto_ml'
    from auto_ml import Predictor
    names = {c: str(i) for (i, c) in enumerate(X_train.columns)}
    X_train.columns = names
    X_test.columns = names
    df_types.loc[((df_types['NAME'] == 'target'), 'TYPE')] = 'output'
    df_types = df_types[(df_types['TYPE'] != 'numerical')].set_index('NAME')
    df_types = df_types.rename(index=names)['TYPE'].to_dict()
    X_train['target'] = y_train
    cmodels = ['AdaBoostClassifier', 'ExtraTreesClassifier', 'RandomForestClassifier', 'XGBClassifier']
    rmodels = ['BayesianRidge', 'ElasticNet', 'Lasso', 'LassoLars', 'LinearRegression', 'Perceptron', 'LogisticRegression', 'AdaBoostRegressor', 'ExtraTreesRegressor', 'PassiveAggressiveRegressor', 'RandomForestRegressor', 'SGDRegressor', 'XGBRegressor']
    automl = Predictor(type_of_estimator=('classifier' if (m_type == 'classification') else 'regressor'), column_descriptions=df_types)
    automl.train(X_train, model_names=(cmodels if (m_type == 'classification') else rmodels), scoring=('f1_score' if (m_type == 'classification') else 'mean_squared_error'), cv=5, verbose=False)
    return (automl.predict_proba(X_test) if (m_type == 'classification') else automl.predict(X_test))

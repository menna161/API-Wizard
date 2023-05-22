import os, time, json, pandas
import pprint as pp
from typing import List, Mapping
import numpy as np
import pandas as pd
from pandas import DataFrame
from tempfile import TemporaryDirectory
from datetime import datetime
from autogluon import TabularPrediction as task
from autogluon.task.tabular_prediction import TabularPredictor
from autogluon.utils.tabular.ml.constants import BINARY, MULTICLASS, REGRESSION
from autogluon_utils.configs.kaggle.constants import *
from autogluon_utils.benchmarking.baselines.h2o_base.h2o_base import H2OBaseline
from autogluon_utils.benchmarking.baselines.tpot_base.tpot_base import TPOTBaseline
from autogluon_utils.benchmarking.baselines.autosklearn_base.autosklearn_base import AutoSklearnBaseline
from autogluon_utils.benchmarking.baselines.autoweka.methods_autoweka import autoweka_fit_predict
from autogluon_utils.benchmarking.baselines.gcp.methods_gcp import gcptables_fit_predict


def run_competition(self, train_data: DataFrame, test_data: DataFrame, competition_meta: Mapping[(str, str)], profile: Mapping[(str, any)], metrics: Mapping[(str, any)], tmp_dir: TemporaryDirectory):
    gcp_info = {'COMPUTE_REGION': 'us-central1', 'PROJECT_ID': GCP_PROJECT_ID, 'BUCKET_NAME': GCP_BUCKET_NAME, 'GOOGLE_APPLICATION_CREDENTIALS': GOOGLE_APPLICATION_CREDENTIALS}
    dataset_name = competition_meta[NAME]
    dataset_name = dataset_name[:13]
    TIMESTAMP_STR = datetime.utcnow().strftime('%Y_%m_%d-%H_%M_%S')
    dataset_name = (dataset_name + TIMESTAMP_STR)
    if (SUBSAMPLE in profile):
        suffix = ('SAMP' + str(profile[SUBSAMPLE]))
        dataset_name = dataset_name[:(32 - len(suffix))]
        dataset_name = (dataset_name + suffix)
    dataset_name = dataset_name[:32]
    print('Fitting GCP Tables...')
    runtime_sec = None
    if ('runtime_hr' in profile):
        print(('with time-limit = %s hr...' % profile['runtime_hr']))
        runtime_sec = int((profile['runtime_hr'] * 3600))
    (num_models_trained, num_models_ensemble, fit_time, y_preds, y_prob, predict_time, class_order) = gcptables_fit_predict(train_data=train_data, test_data=test_data, label_column=competition_meta[LABEL_COLUMN], problem_type=competition_meta[PROBLEM_TYPE], eval_metric=competition_meta[EVAL_METRIC], output_directory=tmp_dir, runtime_sec=runtime_sec, dataset_name=dataset_name, gcp_info=gcp_info)
    if (competition_meta[EVAL_METRIC] in PREDICT_PROBA_METRICS):
        y_preds = y_prob
    metrics['num_models_trained'] = num_models_trained
    metrics['num_models_ensemble'] = num_models_ensemble
    metrics['fit_time'] = fit_time
    metrics['pred_time'] = predict_time
    return (y_preds, class_order)

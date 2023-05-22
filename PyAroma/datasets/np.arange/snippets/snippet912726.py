import json
import keras.backend as K
import logging
import numpy as np
import os
import pickle
import tempfile
import time
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials, pyll
from keras.callbacks import EarlyStopping, ModelCheckpoint
from scipy.stats import pearsonr, spearmanr, kendalltau
from src.BiGRU_experiments.BiGRU_model import compile_bigrus_attention
from hyperopt_output.logs import LOGS_DIR
from hyperopt_output.Trials import TRIALS_DIR
from configuration import CONFIG_DIR
from input import INPUT_DIR


def optimization_function(network, train_samples, test_samples, val_samples, current_space, year, mode, metric):
    "\n    Train the model 'folds' times with the specific parameters (current space) that are chosen by hyper_opt algorithm\n    and given the performance of the model on the test and validation data, writes on the log file the best epoch,\n    the performance of each epoch ('+', '-' increasing-decreasing) with respect to validation loss and\n    the results (correlations) of the model on the validation and test data.\n    :param network: The compiled network ready to be trained.\n    :param train_samples: A dict the will be fed on the network at the training process.\n    :param test_samples: A dict the will be fed on the network at the testing process.\n    :param val_samples: A dict the will be fed on the network at the validation process.\n    :param current_space: A dict with the specific parameters that will be used at the training of the model.\n    :param year: A year that we are testing.\n    :param mode: Depending on your choice : ['Single Task', 'Multi Task-1', 'Multi Task-5'].\n    :param metric: The metric for which the model will be trained. It is needed only on 'Single Task' mode.\n    :return:\n    "
    trial_start = time.time()
    LOGGER.info(((((('\n' + ('=' * 115)) + '\n') + MSG_TEMPLATE.format(TRIAL_NO, HYPER_OPT_CONFIG['trials'], str(current_space['n_hidden_layers']), str(current_space['hidden_units_size']), current_space['batch_size'], current_space['dropout_rate'], current_space['word_dropout_rate'], current_space['attention_mechanism'], current_space['learning_rate'], year, metric, mode)) + '\n') + ('=' * 115)))
    statistics = {method: {} for method in ['validation', 'test']}
    fold_loss = []
    for fold_no in range(HYPER_OPT_CONFIG['folds']):
        LOGGER.info('\n----- Fold: {0}/{1} -----\n'.format((fold_no + 1), HYPER_OPT_CONFIG['folds']))
        indices = np.arange(len(list(train_samples['x'])))
        if (HYPER_OPT_CONFIG['folds'] != 1):
            np.random.seed(fold_no)
            np.random.shuffle(indices)
        early_stopping = EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)
        with tempfile.NamedTemporaryFile(delete=True) as w_fd:
            weights_file = w_fd.name
            model_checkpoint = ModelCheckpoint(filepath=weights_file, monitor='val_loss', mode='auto', verbose=1, save_best_only=True, save_weights_only=True)
            fit_history = network.fit(x=train_samples['x'], y=train_samples['y'], epochs=HYPER_OPT_CONFIG['epochs'], validation_data=(val_samples['x'], val_samples['y']), callbacks=[early_stopping, model_checkpoint], verbose=2)
        best_epoch = (np.argmin(fit_history.history['val_loss']) + 1)
        n_epochs = len(fit_history.history['val_loss'])
        val_loss_per_epoch = ('- ' + ' '.join((('-' if (fit_history.history['val_loss'][i] < np.min(fit_history.history['val_loss'][:i])) else '+') for i in range(1, len(fit_history.history['val_loss'])))))
        LOGGER.info('\nBest epoch: {}/{}'.format(best_epoch, n_epochs))
        LOGGER.info('Val loss per epoch: {}\n'.format(val_loss_per_epoch))
        LOGGER.info('\n----- Validation Results -----')
        val_report_statistics = calculate_performance(network=network, true_samples=val_samples['x'], true_targets=val_samples['y'], ordered_ids=val_samples['ordered_ids'], empty_ids=[], mode=mode, human_metric=metric)
        if ((mode == 'Multi Task-1') or (mode == 'Multi Task-5')):
            for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
                statistics['validation'][q] = val_report_statistics[q]
        else:
            statistics['validation'][metric] = val_report_statistics[metric]
        LOGGER.info('\n----- Test Results ------------')
        test_report_statistics = calculate_performance(network=network, true_samples=test_samples['x'], true_targets=test_samples['y'], ordered_ids=test_samples['ordered_ids'], empty_ids=test_samples['empty_ids'], mode=mode, human_metric=metric)
        if ((mode == 'Multi Task-1') or (mode == 'Multi Task-5')):
            for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
                statistics['test'][q] = test_report_statistics[q]
        else:
            statistics['test'][metric] = test_report_statistics[metric]
        fold_loss.append((1 - val_report_statistics[metric]['Spearman']))
    LOGGER.info('Trial training took {0} sec\n'.format(time.strftime('%H:%M:%S', time.gmtime((time.time() - trial_start)))))
    current_space['trial_no'] = TRIAL_NO
    return {'loss': np.average(fold_loss), 'status': STATUS_OK, 'trial_no': TRIAL_NO, 'results': {'configuration': current_space, 'time': (time.time() - trial_start), 'statistics': statistics}}

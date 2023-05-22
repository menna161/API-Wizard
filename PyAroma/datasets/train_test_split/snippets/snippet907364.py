import mlopt.settings as stg
import mlopt.learners.pytorch.settings as pts
from optuna.integration import PyTorchLightningPruningCallback
from pytorch_lightning import Trainer
from mlopt.learners.pytorch.lightning import LightningNet
from pytorch_lightning import Callback
import mlopt.error as e
from mlopt.learners.learner import Learner
from sklearn.model_selection import train_test_split
import optuna
from time import time
import os
import logging
import torch
import torch


def train(self, X, y):
    '\n        Train model.\n\n        Parameters\n        ----------\n        X : pandas DataFrame\n            Features.\n        y : numpy int array\n            Labels.\n        '
    self.n_train = len(X)
    (X_train, X_valid, y_train, y_valid) = train_test_split(X, y, test_size=(1 - stg.FRAC_TRAIN), random_state=0)
    data = {'X_train': X_train, 'y_train': y_train, 'X_valid': X_valid, 'y_valid': y_valid}
    stg.logger.info(('Split dataset in %d training and %d validation' % (len(y_train), len(y_valid))))
    start_time = time()
    objective = PytorchObjective(data, self.options['bounds'], self.n_input, self.n_classes, self.use_gpu)
    sampler = optuna.samplers.TPESampler(seed=0)
    pruner = optuna.pruners.MedianPruner()
    study = optuna.create_study(sampler=sampler, pruner=pruner, direction='minimize')
    study.optimize(objective, n_trials=self.options['n_train_trials'])
    self.best_params = study.best_trial.params
    self.best_params['n_input'] = self.n_input
    self.best_params['n_classes'] = self.n_classes
    self.print_trial_stats(study)
    stg.logger.info('Train with best parameters')
    self.trainer = Trainer(checkpoint_callback=False, accelerator='dp', logger=False, max_epochs=self.best_params['max_epochs'], gpus=((- 1) if self.use_gpu else None))
    self.model = LightningNet(self.best_params, data)
    self.trainer.fit(self.model)
    end_time = time()
    stg.logger.info(('Training time %.2f' % (end_time - start_time)))

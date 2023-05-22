import logging
import os
from argparse import ArgumentParser, Namespace
from distutils.util import strtobool
from enum import Enum
from typing import Any, Callable, List
import torch
from agent.config import args
from agent.config import model_args
from agent.evaluation import metric


def get_optimizer(self, task: model_args.Task, finetune: bool=False) -> Callable[([Any], torch.optim.Optimizer)]:
    self.check_initialized()
    learning_rate: float = 0.0
    l2_coefficient: float = 0.0
    if (task == model_args.Task.PLAN_PREDICTOR):
        learning_rate = self._plan_prediction_learning_rate
        l2_coefficient = self._plan_prediction_l2_coefficient
    elif (task == model_args.Task.ACTION_GENERATOR):
        if finetune:
            learning_rate = self._finetune_learning_rate
            l2_coefficient = self._finetune_l2_coefficient
        else:
            learning_rate = self._action_generation_learning_rate
            l2_coefficient = self._action_generation_l2_coefficient
    if (self._optimizer_type == OptimizerType.ADAM):
        logging.info(((('Adam with lr = ' + str(learning_rate)) + ', weight decay = ') + str(l2_coefficient)))
        return (lambda params: torch.optim.Adam(params, lr=learning_rate, weight_decay=l2_coefficient))
    elif (self._optimizer_type == OptimizerType.ADAGRAD):
        logging.info(((('Adagrad with lr = ' + str(learning_rate)) + ', weight decay = ') + str(l2_coefficient)))
        return (lambda params: torch.optim.Adagrad(params, lr=learning_rate, weight_decay=l2_coefficient))
    elif (self._optimizer_type == OptimizerType.RMSPROP):
        logging.info(((('RMSProp with lr = ' + str(learning_rate)) + ', weight decay = ') + str(l2_coefficient)))
        return (lambda params: torch.optim.RMSprop(params, lr=learning_rate, weight_decay=l2_coefficient))
    elif (self._optimizer_type == OptimizerType.SGD):
        logging.info(((('SGD with lr = ' + str(learning_rate)) + ', weight decay = ') + str(l2_coefficient)))
        return (lambda params: torch.optim.SGD(params, lr=learning_rate, weight_decay=l2_coefficient))

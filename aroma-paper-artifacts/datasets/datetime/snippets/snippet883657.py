import os
import os.path as path
import datetime
import torch
import logging
import numpy as np
import sonosco.common.path_utils as path_utils
import sonosco.common.utils as utils
from random import random
from typing import TypeVar
from .trainer import ModelTrainer
from .callbacks.model_checkpoint import ModelCheckpoint
from .tb_callbacks import TensorBoardCallback
from sonosco.serialization import Serializer
from time import time


@staticmethod
def _set_experiment_name(experiment_name: str) -> str:
    '\n        Set experiment name.\n\n        Args:\n            experiment_name: experiment name\n\n        Returns: timestamped experiment name\n\n        '
    date_time = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H:%M:%S')
    return f'{date_time}_{experiment_name}'

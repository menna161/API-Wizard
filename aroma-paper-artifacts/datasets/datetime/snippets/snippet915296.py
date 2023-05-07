import datetime
import json
import logging
import os
import torch
from machamp.model.machamp import MachampModel
from uniplot import plot_to_string


def __init__(self, serialization_dir, num_epochs, keep_best_n: int=1):
    '\n        Class that keeps track of performance of models over epochs\n        and handles model saving where necessary.\n\n        Parameters\n        ----------\n        keep_best_n: int\n            the amount of models to keep\n        '
    self.keep_best_n = keep_best_n
    self.serialization_dir = serialization_dir
    self.num_epochs = num_epochs
    self.start_time = datetime.datetime.now()
    self.epoch_start_time = datetime.datetime.now()
    self.sums = {}
    self.dev_scores = []
    self.train_scores = []
    self.dev_losses = []
    self.train_losses = []

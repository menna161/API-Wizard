import datetime
import json
import logging
import os
import torch
from machamp.model.machamp import MachampModel
from uniplot import plot_to_string


def start_epoch_timer(self):
    self.epoch_start_time = datetime.datetime.now()

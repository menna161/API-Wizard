import os
import sys
import argparse
import yaml
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torchlight
from torchlight import str2bool
from torchlight import DictAction
from torchlight import import_class
from .processor import Processor
from .data_tools import *


def load_optimizer(self):
    if (self.arg.optimizer == 'SGD'):
        self.optimizer = optim.SGD(params=self.model.parameters(), lr=self.arg.base_lr, momentum=0.9, nesterov=self.arg.nesterov, weight_decay=self.arg.weight_decay)
    elif (self.arg.optimizer == 'Adam'):
        self.optimizer = optim.Adam(params=self.model.parameters(), lr=self.arg.base_lr, weight_decay=self.arg.weight_decay)

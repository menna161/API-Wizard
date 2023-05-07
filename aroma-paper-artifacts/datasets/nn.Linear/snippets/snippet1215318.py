from __future__ import print_function, division
import os
import torch
import torch.nn as nn
import numpy as np
import random
import copy


def __init__(self, in_size, drop_rate, fil_num):
    super(_MLP_D, self).__init__()
    self.fc1 = nn.Linear(in_size, fil_num)
    self.fc2 = nn.Linear(fil_num, 2)
    self.do1 = nn.Dropout(drop_rate)
    self.do2 = nn.Dropout(drop_rate)
    self.ac1 = nn.LeakyReLU()

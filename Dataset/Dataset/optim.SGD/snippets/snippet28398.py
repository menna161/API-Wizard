import os
import copy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm
from utils import *
import time
import numpy as np
import warnings
import pdb


def init_optimizers(self, optim_params):
    optimizer = optim.SGD(optim_params)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=self.scheduler_params['step_size'], gamma=self.scheduler_params['gamma'])
    return (optimizer, scheduler)

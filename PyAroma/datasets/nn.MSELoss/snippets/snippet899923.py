import os
import torch
import torch.optim as optim
import torch.nn as nn
from abc import abstractmethod
from tensorboardX import SummaryWriter
from util.utils import TrainClock


def set_loss_function(self):
    'set loss function used in training'
    self.criterion = nn.MSELoss().cuda()

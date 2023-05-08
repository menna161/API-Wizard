import os
import torch.distributed as dist
import torch
import torch.nn as nn
from .xception import xception
from utils import print_with_rank


def __init__(self, modelchoice, num_out_classes=2, pretrain_path=None, dropout=None):
    super(TransferModel, self).__init__()
    self.modelchoice = modelchoice
    if (modelchoice == 'xception'):
        self.model = return_pytorch04_xception(pretrain_path=pretrain_path)
        num_ftrs = self.model.fc.in_features
        if (not dropout):
            self.model.fc = nn.Linear(num_ftrs, num_out_classes)
        else:
            print('Using dropout', dropout)
            self.model.fc = nn.Sequential(nn.Dropout(p=dropout), nn.Linear(num_ftrs, num_out_classes))
    else:
        raise Exception('Choose valid model, e.g. resnet50')

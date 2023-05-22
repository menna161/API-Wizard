import torch
from torch.utils.data import DataLoader, WeightedRandomSampler
import os
from sklearn.metrics import roc_auc_score
from models.nfm import NeuralFactorizationMachineModel
from models.hen import HENModel
from models.m3r import SeqM3RModel
from models.wd import WideAndDeepModel
from models.lstm4fd import LSTM4FDModel
from data.dataset import Mydataset
import time
from utils.utils import mmd_rbf_noaccelerate, cmmd, coral, euclidian, c_euclidian, nometric, ced
from utils.utils import Stoper, Averager
import math
import argparse


def get_model(name, field_dims):
    '\n    name: the name of the target model\n    field_dims: the dimensions of fields\n    '
    if (name == 'nfm'):
        return NeuralFactorizationMachineModel(field_dims, embed_dim=16, mlp_dims=(64,), dropouts=(0.2, 0.2))
    elif (name == 'hen'):
        return HENModel(field_dims, embed_dim=16, sequence_length=11, lstm_dims=20, mlp_dims=(64,), dropouts=(0.2, 0.2))
    elif (name == 'wd'):
        return WideAndDeepModel(field_dims, embed_dim=16, mlp_dims=(64,), dropout=0.2)
    elif (name == 'lstm4fd'):
        return LSTM4FDModel(field_dims, embed_dim=16, sequence_length=11, lstm_dims=20, mlp_dims=(64,), dropouts=(0.2, 0.2))
    elif (name == 'm3r'):
        return SeqM3RModel(field_dims, embed_dim=16, sequence_length=11, lstm_dims=20, mlp_dims=(64,), dropouts=(0.2, 0.2))
    else:
        raise ValueError(('unknown model name: ' + name))

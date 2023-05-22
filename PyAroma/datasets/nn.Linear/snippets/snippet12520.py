from encoder.params_model import *
from encoder.params_data import *
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve
from torch.nn.utils import clip_grad_norm_
from scipy.optimize import brentq
from torch import nn
import numpy as np
import torch


def __init__(self, device, loss_device):
    super().__init__()
    self.loss_device = loss_device
    self.lstm = nn.LSTM(input_size=mel_n_channels, hidden_size=model_hidden_size, num_layers=model_num_layers, batch_first=True).to(device)
    self.linear = nn.Linear(in_features=model_hidden_size, out_features=model_embedding_size).to(device)
    self.relu = torch.nn.ReLU().to(device)
    self.similarity_weight = nn.Parameter(torch.tensor([10.0])).to(loss_device)
    self.similarity_bias = nn.Parameter(torch.tensor([(- 5.0)])).to(loss_device)
    self.loss_fn = nn.CrossEntropyLoss().to(loss_device)

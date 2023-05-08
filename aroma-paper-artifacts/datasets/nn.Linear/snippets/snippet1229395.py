import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
from scipy.special import softmax
import time
import math
from sklearn.metrics import roc_auc_score, average_precision_score
from scipy import stats
from torch.nn.modules.loss import CrossEntropyLoss


def __build(self, stddev=0.0001, seed=3):
    "\n\t\tBuilds the model's linear layers and initializes them.\n\t\t"
    torch.manual_seed(3)
    W = {}
    self.nlayer = len(self.nhidden)
    for i in range(1, self.nlayer):
        W[str(i)] = nn.Linear(self.nhidden[(i - 1)], self.nhidden[i]).requires_grad_()
        nn.init.xavier_uniform_(W[str(i)].weight)
        nn.init.zeros_(W[str(i)].bias)
    self.W = nn.ModuleDict(W)

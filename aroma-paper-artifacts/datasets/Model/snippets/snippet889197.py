import torch
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import tqdm
from tensorflow import keras
from metamodel import MetaModel
from sklearn.metrics import roc_auc_score
import pickle
from utils import Averager, Stoper
import copy
import math
import random


def get_model(self):
    if (self.base_model_name == 'WD'):
        model = MetaModel(col_names=self.columns, max_ids=self.max_ids, embed_dim=self.emb_dim, mlp_dims=self.mlp_dims, dropout=self.dropout, use_cuda=self.use_cuda, local_lr=self.local_train_lr, global_lr=self.global_lr, weight_decay=self.weight_decay, base_model_name=self.base_model_name, num_expert=self.num_expert, num_output=self.num_output)
    else:
        raise ValueError(('Unknown base model: ' + self.base_model_name))
    return (model.cuda() if self.use_cuda else model)

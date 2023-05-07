import os
import numpy as np
from model import _CNN, _FCN, _MLP_A, _MLP_B, _MLP_C, _MLP_D
from utils import matrix_sum, get_accu, get_MCC, get_confusion_matrix, write_raw_score, DPM_statistics, timeit, read_csv
from dataloader import CNN_Data, FCN_Data, MLP_Data, MLP_Data_apoe, CNN_MLP_Data
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
from tqdm import tqdm
import numpy as np


def valid_model_epoch(self):
    with torch.no_grad():
        self.model.train(False)
        valid_matrix = [[0, 0], [0, 0]]
        for (inputs, labels, demors) in self.valid_dataloader:
            (inputs, labels, demors) = (inputs, labels, demors)
            preds = self.model(inputs, demors)
            valid_matrix = matrix_sum(valid_matrix, get_confusion_matrix(preds, labels))
    return valid_matrix

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


def test(self, repe_idx):
    accu_list = []
    self.model.load_state_dict(torch.load('{}{}_{}.pth'.format(self.checkpoint_dir, self.model_name, self.optimal_epoch)))
    self.model.train(False)
    with torch.no_grad():
        for stage in ['train', 'valid', 'test', 'AIBL', 'NACC', 'FHS']:
            data = MLP_Data_apoe(self.Data_dir, self.exp_idx, stage=stage, roi_threshold=self.roi_threshold, roi_count=self.roi_count, choice=self.choice, seed=self.seed)
            dataloader = DataLoader(data, batch_size=10, shuffle=False)
            f = open((self.checkpoint_dir + 'raw_score_{}_{}.txt'.format(stage, repe_idx)), 'w')
            matrix = [[0, 0], [0, 0]]
            for (idx, (inputs, labels, demors)) in enumerate(dataloader):
                (inputs, labels, demors) = (inputs, labels, demors)
                preds = self.model(inputs, demors)
                write_raw_score(f, preds, labels)
                matrix = matrix_sum(matrix, get_confusion_matrix(preds, labels))
            f.close()
            accu_list.append(self.eval_metric(matrix))
    return accu_list

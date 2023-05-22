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


def test(self):
    print('testing ... ')
    self.model.load_state_dict(torch.load('{}{}_{}.pth'.format(self.checkpoint_dir, self.model_name, self.optimal_epoch)))
    self.model.train(False)
    with torch.no_grad():
        for stage in ['train', 'valid', 'test', 'AIBL', 'NACC', 'FHS']:
            Data_dir = self.Data_dir
            if (stage in ['AIBL', 'NACC', 'FHS']):
                Data_dir = Data_dir.replace('ADNI', stage)
            data = CNN_Data(Data_dir, self.exp_idx, stage=stage, seed=self.seed)
            dataloader = DataLoader(data, batch_size=10, shuffle=False)
            f = open((self.checkpoint_dir + 'raw_score_{}.txt'.format(stage)), 'w')
            matrix = [[0, 0], [0, 0]]
            for (idx, (inputs, labels)) in enumerate(dataloader):
                (inputs, labels) = (inputs.cuda(), labels.cuda())
                preds = self.model(inputs)
                write_raw_score(f, preds, labels)
                matrix = matrix_sum(matrix, get_confusion_matrix(preds, labels))
            print((stage + ' confusion matrix '), matrix, ' accuracy ', self.eval_metric(matrix))
            f.close()

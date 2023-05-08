import torch
import torch.utils.data as data
import torchnet as tnt
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
import os
import json
import pickle as pkl
import argparse
import pprint
from models.stclassifier import PseTae, PseLTae, PseGru, PseTempCNN
from dataset import PixelSetData, PixelSetData_preloaded
from learning.focal_loss import FocalLoss
from learning.weight_init import weight_init
from learning.metrics import mIou, confusion_matrix_analysis


def overall_performance(config):
    cm = np.zeros((config['num_classes'], config['num_classes']))
    for fold in range(1, (config['kfold'] + 1)):
        cm += pkl.load(open(os.path.join(config['res_dir'], 'Fold_{}'.format(fold), 'conf_mat.pkl'), 'rb'))
    (_, perf) = confusion_matrix_analysis(cm)
    print('Overall performance:')
    print('Acc: {},  IoU: {}'.format(perf['Accuracy'], perf['MACRO_IoU']))
    with open(os.path.join(config['res_dir'], 'overall.json'), 'w') as file:
        file.write(json.dumps(perf, indent=4))

from __future__ import division
from tools.model import load_model
from config.configs_kf import *
from lib.utils.visual import *
import torchvision.transforms as st
from sklearn.metrics import confusion_matrix
import numpy as np
from tqdm import tqdm_notebook as tqdm
from tools.ckpt import *
import time
import itertools


def metrics(predictions, gts, label_values=land_classes):
    cm = confusion_matrix(gts, predictions, range(len(label_values)))
    print('Confusion matrix :')
    print(cm)
    print('---')
    total = sum(sum(cm))
    accuracy = sum([cm[x][x] for x in range(len(cm))])
    accuracy *= (100 / float(total))
    print('{} pixels processed'.format(total))
    print('Total accuracy : {}%'.format(accuracy))
    print('---')
    F1Score = np.zeros(len(label_values))
    for i in range(len(label_values)):
        try:
            F1Score[i] = ((2.0 * cm[(i, i)]) / (np.sum(cm[(i, :)]) + np.sum(cm[(:, i)])))
        except BaseException:
            pass
    print('F1Score :')
    for (l_id, score) in enumerate(F1Score):
        print('{}: {}'.format(label_values[l_id], score))
    print('---')
    total = np.sum(cm)
    pa = (np.trace(cm) / float(total))
    pe = (np.sum((np.sum(cm, axis=0) * np.sum(cm, axis=1))) / float((total * total)))
    kappa = ((pa - pe) / (1 - pe))
    print(('Kappa: ' + str(kappa)))
    return (accuracy, cm)

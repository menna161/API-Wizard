from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.metrics import precision_recall_curve, average_precision_score
from scipy import interp
from collections import defaultdict
import numpy as np
import math
import csv


def calc_neurologist_statistics(y, y_pred_list):
    (rslt, sens, spcs, prcs) = ({}, [], [], [])
    for (i, y_pred) in enumerate(y_pred_list):
        (TN, FP, FN, TP) = confusion_matrix(y, y_pred).ravel()
        sens.append((TP / (TP + FN)))
        spcs.append((TN / (TN + FP)))
        prcs.append((TP / (TP + FP)))
        rslt['neorologist_{}'.format(i)] = {'sensitivity': sens[(- 1)], 'specificity': spcs[(- 1)], 'precision': prcs[(- 1)]}
    rslt['mean'] = {'sensitivity': np.mean(sens), 'specificity': np.mean(spcs), 'precision': np.mean(prcs)}
    rslt['std'] = {'sensitivity': np.std(sens), 'specificity': np.std(spcs), 'precision': np.std(prcs)}
    return rslt

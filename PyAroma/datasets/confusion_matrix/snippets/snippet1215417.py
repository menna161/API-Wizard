from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.metrics import precision_recall_curve, average_precision_score
from scipy import interp
from collections import defaultdict
import numpy as np
import math
import csv


def calc_performance_statistics(all_scores, y):
    statistics = {}
    y_pred_all = np.argmax(all_scores, axis=2)
    statistics = defaultdict(list)
    for y_pred in y_pred_all:
        (TN, FP, FN, TP) = confusion_matrix(y, y_pred).ravel()
        N = (((TN + TP) + FN) + FP)
        S = ((TP + FN) / N)
        P = ((TP + FP) / N)
        acc = ((TN + TP) / N)
        sen = (TP / (TP + FN))
        spc = (TN / (TN + FP))
        prc = (TP / (TP + FP))
        f1s = ((2 * (prc * sen)) / (prc + sen))
        mcc = (((TP / N) - (S * P)) / np.sqrt((((P * S) * (1 - S)) * (1 - P))))
        statistics['confusion_matrix'].append(confusion_matrix(y, y_pred))
        statistics['accuracy'].append(acc)
        statistics['sensitivity'].append(sen)
        statistics['specificity'].append(spc)
        statistics['precision'].append(prc)
        statistics['f1_score'].append(f1s)
        statistics['MCC'].append(mcc)
    return statistics

from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.metrics import precision_recall_curve, average_precision_score
from scipy import interp
from collections import defaultdict
import numpy as np
import math
import csv


def load_neurologist_data(fn):
    with open(fn, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = list(csv_reader)
    rows = np.array(rows)
    rows = rows[(1:, 4:)]
    rows[(rows == 'AD')] = 1
    rows[(rows == 'NL')] = 0
    rslt = {'y': rows[(:, 0)].astype(np.int), 'y_pred_list': rows[(:, 1:)].T.astype(np.int)}
    return rslt

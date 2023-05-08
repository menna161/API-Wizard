import numpy as np
import pandas as pd


def confusion_matrix_analysis(mat):
    '\n    This method computes all the performance metrics from the confusion matrix. In addition to overall accuracy, the\n    precision, recall, f-score and IoU for each class is computed.\n    The class-wise metrics are averaged to provide overall indicators in two ways (MICRO and MACRO average)\n    Args:\n        mat (array): confusion matrix\n\n    Returns:\n        per_class (dict) : per class metrics\n        overall (dict): overall metrics\n\n    '
    TP = 0
    FP = 0
    FN = 0
    per_class = {}
    for j in range(mat.shape[0]):
        d = {}
        tp = np.sum(mat[(j, j)])
        fp = (np.sum(mat[(:, j)]) - tp)
        fn = (np.sum(mat[(j, :)]) - tp)
        d['IoU'] = (tp / ((tp + fp) + fn))
        d['Precision'] = (tp / (tp + fp))
        d['Recall'] = (tp / (tp + fn))
        d['F1-score'] = ((2 * tp) / (((2 * tp) + fp) + fn))
        per_class[str(j)] = d
        TP += tp
        FP += fp
        FN += fn
    overall = {}
    overall['micro_IoU'] = (TP / ((TP + FP) + FN))
    overall['micro_Precision'] = (TP / (TP + FP))
    overall['micro_Recall'] = (TP / (TP + FN))
    overall['micro_F1-score'] = ((2 * TP) / (((2 * TP) + FP) + FN))
    macro = pd.DataFrame(per_class).transpose().mean()
    overall['MACRO_IoU'] = macro.loc['IoU']
    overall['MACRO_Precision'] = macro.loc['Precision']
    overall['MACRO_Recall'] = macro.loc['Recall']
    overall['MACRO_F1-score'] = macro.loc['F1-score']
    overall['Accuracy'] = (np.sum(np.diag(mat)) / np.sum(mat))
    return (per_class, overall)

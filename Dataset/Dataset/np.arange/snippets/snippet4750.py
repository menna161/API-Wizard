from __future__ import print_function, division
import numpy as np
from sklearn.metrics import confusion_matrix


def evaluate(predictions, gts, num_classes):
    conmatrix = np.zeros((num_classes, num_classes))
    labels = np.arange(num_classes).tolist()
    for (lp, lt) in zip(predictions, gts):
        lp[(lt == 255)] = 255
        conmatrix += confusion_matrix(lt.flatten(), lp.flatten(), labels=labels)
    (M, N) = conmatrix.shape
    tp = np.zeros(M, dtype=np.uint)
    fp = np.zeros(M, dtype=np.uint)
    fn = np.zeros(M, dtype=np.uint)
    for i in range(M):
        tp[i] = conmatrix[(i, i)]
        fp[i] = (np.sum(conmatrix[(:, i)]) - tp[i])
        fn[i] = (np.sum(conmatrix[(i, :)]) - tp[i])
    precision = (tp / (tp + fp))
    recall = (tp / (tp + fn))
    f1_score = (((2 * recall) * precision) / (recall + precision))
    ax_p = 0
    acc = (np.diag(conmatrix).sum() / conmatrix.sum())
    acc_cls = (np.diag(conmatrix) / conmatrix.sum(axis=ax_p))
    acc_cls = np.nanmean(acc_cls)
    iu = (tp / ((tp + fp) + fn))
    mean_iu = np.nanmean(iu)
    freq = (conmatrix.sum(axis=ax_p) / conmatrix.sum())
    fwavacc = (freq[(freq > 0)] * iu[(freq > 0)]).sum()
    return (acc, acc_cls, mean_iu, fwavacc, np.nanmean(f1_score))

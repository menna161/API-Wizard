import numpy as np


def ErrorRateAt95Recall(labels, scores):
    distances = (1.0 / (scores + 1e-08))
    recall_point = 0.95
    labels = labels[np.argsort(distances)]
    threshold_index = np.argmax((np.cumsum(labels) >= (recall_point * np.sum(labels))))
    FP = np.sum((labels[:threshold_index] == 0))
    TN = np.sum((labels[threshold_index:] == 0))
    return (float(FP) / float((FP + TN)))

import argparse
from pathlib import Path
import numpy as np
import re


def generate_confusion_matrix(zipped):
    '\n    Creates a confusion matrix from two aligned data sets\n    :param zipped: an array of tuples representing 2 arrays joined by index\n    :return: an MxM matrix of predictions vs truth\n    '
    invalid_labels = []
    dim = len(LABELS)
    matrix = np.zeros((dim, (dim + 1)), np.uint)
    skipped_count = 0
    for (truth_val, prediction_val) in zipped:
        truth_index = LABEL_INDEXES.get(truth_val)
        prediction_index = LABEL_INDEXES.get(prediction_val)
        if (truth_index is None):
            skipped_count += 1
            if (truth_val == NULL_CLASS):
                continue
            if (truth_val not in invalid_labels):
                print('Invalid truth LABEL: {}'.format(truth_val))
                invalid_labels.append(truth_val)
            continue
        if (prediction_index is None):
            if (prediction_val not in invalid_labels):
                invalid_labels.append(prediction_val)
                print('Invalid prediction LABEL: {}'.format(prediction_val))
            prediction_index = (- 1)
        matrix[truth_index][prediction_index] += 1
    if skipped_count:
        print('Skipped {} unlabeled truth points'.format(skipped_count))
    return matrix

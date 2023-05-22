import argparse
from pathlib import Path
import numpy as np
import re


def score_prediction_files(ground_truth_file, prediction_file):
    '\n    Scores a list of prediction files\n    :param ground_truth_file: Ground truth classification file\n    :param prediction_files: Array of classification prediction files\n    :return: None\n    '
    print('Scoring {} against {}:'.format(prediction_file, ground_truth_file))
    dim = len(LABELS)
    confusion_matrix = np.zeros((dim, (dim + 1)), np.uint)
    with open(str(ground_truth_file), 'r') as file:
        try:
            gt_data = [int(line) for line in file]
        except ValueError:
            print('Error reading {}'.format(ground_truth_file))
            return confusion_matrix
    with open(str(prediction_file), 'r') as file:
        try:
            pd_data = [int(line) for line in file]
        except ValueError:
            print('Error reading {}'.format(ground_truth_file))
            return confusion_matrix
    if (len(gt_data) != len(pd_data)):
        print('Mismatched file lengths!')
        return confusion_matrix
    one_to_one = zip(gt_data, pd_data)
    confusion_matrix = generate_confusion_matrix(one_to_one)
    print('Scores for {} (truth: {}):'.format(prediction_file, ground_truth_file))
    report_scores(confusion_matrix)
    return confusion_matrix

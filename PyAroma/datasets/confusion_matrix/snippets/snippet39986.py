import argparse
from pathlib import Path
import numpy as np
import re

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--ground_truth_directory', type=directory_type)
    parser.add_argument('-t', '--ground_truth_file', type=file_type)
    parser.add_argument('-d', '--prediction_directory', type=directory_type)
    parser.add_argument('-f', '--prediction_file', type=file_type)
    args = parser.parse_args()
    truth_files = []
    if (args.ground_truth_file is not None):
        truth_files.append(args.ground_truth_file)
    if (args.ground_truth_directory is not None):
        truth_files.extend(get_list_of_files(args.ground_truth_directory))
    if (not truth_files):
        raise ValueError('No ground truth paths specified')
    prediction_files = []
    if (args.prediction_file is not None):
        prediction_files.append(args.prediction_file)
    if (args.prediction_directory is not None):
        prediction_files.extend(get_list_of_files(args.prediction_directory))
    if (not prediction_files):
        raise ValueError('No prediction paths specified')
    file_pairs = match_file_pairs(truth_files, prediction_files)
    if (not (type(file_pairs) == list)):
        file_pairs = [file_pairs]
    confusion_matrix = np.zeros((len(LABELS), (len(LABELS) + 1)), np.uint)
    for file_pair in file_pairs:
        confusion_matrix += score_prediction_files(*file_pair)
    if (len(file_pairs) > 1):
        print('----- OVERALL SCORES -----')
        report_scores(confusion_matrix)

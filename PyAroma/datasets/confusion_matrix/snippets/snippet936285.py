import argparse
import os
import sys
import warnings
from uuid import uuid4


def init_main_args():
    'Init command line args used for configuration.'
    parser = argparse.ArgumentParser(description='Runs experiment using LogClass Framework', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--raw_logs', metavar='raw_logs', type=str, nargs=1, help='input raw logs file path')
    base_dir_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
    parser.add_argument('--base_dir', metavar='base_dir', type=str, nargs=1, default=[base_dir_default], help='base output directory for pipeline output files')
    parser.add_argument('--logs', metavar='logs', type=str, nargs=1, help='input logs file path and output for raw logs preprocessing')
    parser.add_argument('--models_dir', metavar='models_dir', type=str, nargs=1, help='trained models input/output directory path')
    parser.add_argument('--features_dir', metavar='features_dir', type=str, nargs=1, help='trained features_dir input/output directory path')
    parser.add_argument('--logs_type', metavar='logs_type', type=str, nargs=1, default=['open_Apache'], choices=['bgl', 'open_Apache', 'open_bgl', 'open_hadoop', 'open_hdfs', 'open_hpc', 'open_proxifier', 'open_zookeeper'], help='Input type of logs.')
    parser.add_argument('--kfold', metavar='kfold', type=int, nargs=1, help='kfold crossvalidation')
    parser.add_argument('--healthy_label', metavar='healthy_label', type=str, nargs=1, default=['unlabeled'], help='the labels of unlabeled logs')
    parser.add_argument('--features', metavar='features', type=str, nargs='+', default=['tfilf'], choices=['tfidf', 'tfilf', 'length', 'tf'], help='Features to be extracted from the logs messages.')
    parser.add_argument('--report', metavar='report', type=str, nargs='+', default=['confusion_matrix'], choices=['confusion_matrix', 'acc', 'multi_acc', 'top_k_svm', 'micro', 'macro'], help='Reports to be generated from the model and its predictions.')
    parser.add_argument('--binary_classifier', metavar='binary_classifier', type=str, nargs=1, default=['pu_learning'], choices=['pu_learning', 'regular'], help='Binary classifier to be used as anomaly detector.')
    parser.add_argument('--multi_classifier', metavar='multi_classifier', type=str, nargs=1, default=['svm'], choices=['svm'], help='Multi-clas classifier to classify anomalies.')
    parser.add_argument('--train', action='store_true', default=False, help=('If set, logclass will train on the given data. Otherwise' + 'it will run inference on it.'))
    parser.add_argument('--force', action='store_true', default=False, help='Force training overwriting previous output with same id.')
    parser.add_argument('--id', metavar='id', type=str, nargs=1, help='Experiment id. Automatically generated if not specified.')
    parser.add_argument('--swap', action='store_true', default=False, help='Swap testing/training data in kfold cross validation.')
    return parser

import random
import copy
from os.path import join, dirname, abspath
import sys
import torch
import numpy as np
import pandas as pd
import evidence_inference.preprocess.preprocessor as preprocessor
from evidence_inference.models.regression import bag_of_words, train_model, test_model
import torch.nn as nn
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
from evidence_inference.models.scan_regression import ScanNet
from evidence_inference.models.scan_regression import train_reformat, scan_reform, Bag_of_words


def run_lr_pipeline(iterations, use_test, path='./model_lr.pth'):
    (x_train, y_train, x_val, y_val, x_test, y_test) = load_data(use_test, path)
    y_test += 1
    print('Loaded {} training examples, {} validation examples, {} testing examples'.format(len(x_train), len(x_val), len(x_test)))
    model = train_model(x_train, y_train, x_val, y_val, iterations, learning_rate=0.001)
    preds = test_model(model, x_test)
    preds = preds
    y_test = y_test.cpu()
    print(classification_report(y_test, preds))
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average='macro')
    prec = precision_score(y_test, preds, average='macro')
    rec = recall_score(y_test, preds, average='macro')
    print(acc)
    print(f1)
    print(prec)
    print(rec)
    print('\n\n')
    return (acc, f1, prec, rec)

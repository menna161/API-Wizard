from os.path import join, dirname, abspath
import sys
import copy
import torch
import random
import numpy as np
import pandas as pd
import evidence_inference.preprocess.preprocessor as preprocessor
import torch.nn as nn
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer


def train_model(x_train, y_train_e, x_val, y_val_e, num_epochs, learning_rate):
    '\n    Train the model using the data given, along with the parameters given.\n\n    @param x_train       is the training dataset.\n    @param y_train_e     is an np.array of the training labels.\n    @param x_val         is the validation set.\n    @param y_val_e       is the np.array of validation labels.\n    @param num_epochs    for the model to use.\n    @param learning_rate for the model to use.\n    @return              the best trained model thus far (based on validation accuracy).\n    '
    y_train_e += 1
    y_val_e += 1
    model = nn.Linear(x_val.shape[1], 3)
    model.float()
    criterion = nn.CrossEntropyLoss(reduction='sum')
    if USE_CUDA:
        model = model.cuda()
        criterion = criterion.cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    best_model = None
    best_accuracy = float('-inf')
    for epoch in range(num_epochs):
        for i in range(len(x_train)):
            tmp = x_train[i].reshape((- 1), len(x_train[i]))
            output = model(tmp)
            loss = criterion(output, y_train_e[i])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            preds = test_model(model, x_val)
        preds = preds
        y_val_e = y_val_e.cpu()
        acc = accuracy_score(y_val_e, preds)
        if (acc > best_accuracy):
            print('Best acc: {:.3f}'.format(acc))
            best_accuracy = acc
            best_model = copy.deepcopy(model)
        print('Epoch: {}, validation accuracy: {:.3f}'.format((epoch + 1), acc))
    return best_model

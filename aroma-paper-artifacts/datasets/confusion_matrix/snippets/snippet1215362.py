import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from numpy import random
import json
import csv
import random
import os
import time


def get_confusion_matrix(preds, labels):
    labels = labels.data.cpu().numpy()
    preds = preds.data.cpu().numpy()
    matrix = [[0, 0], [0, 0]]
    for (index, pred) in enumerate(preds):
        if (np.amax(pred) == pred[0]):
            if (labels[index] == 0):
                matrix[0][0] += 1
            if (labels[index] == 1):
                matrix[0][1] += 1
        elif (np.amax(pred) == pred[1]):
            if (labels[index] == 0):
                matrix[1][0] += 1
            if (labels[index] == 1):
                matrix[1][1] += 1
    return matrix

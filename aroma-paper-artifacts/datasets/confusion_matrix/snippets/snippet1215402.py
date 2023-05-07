from utils_stat import get_roc_info, get_pr_info, calc_neurologist_statistics, read_raw_score
import matplotlib.pyplot as plt
from utils_plot import plot_curve, plot_legend, plot_neorologist
from time import time
import numpy as np


def confusion_matrix(labels, scores):
    matrix = [[0, 0], [0, 0]]
    for (label, pred) in zip(labels, scores):
        if (pred < 0.5):
            if (label == 0):
                matrix[0][0] += 1
            if (label == 1):
                matrix[0][1] += 1
        else:
            if (label == 0):
                matrix[1][0] += 1
            if (label == 1):
                matrix[1][1] += 1
    return matrix

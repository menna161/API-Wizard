from utils_stat import get_roc_info, get_pr_info, calc_neurologist_statistics, read_raw_score
import matplotlib.pyplot as plt
from utils_plot import plot_curve, plot_legend, plot_neorologist
from time import time
import numpy as np

if (__name__ == '__main__'):
    Matrix = []
    for i in range(10):
        (labels, scores) = read_raw_score('../checkpoint_dir/Vol_RF/raw_score_{}.txt'.format(i))
        Matrix.append(confusion_matrix(labels, scores))
    stat_metric(Matrix)

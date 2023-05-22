import torch
import torchvision
import os
import math
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap


def visualize_confusion(writer, step, matrix, class_dict, save_path):
    '\n    Visualization of confusion matrix. Is saved to hard-drive and TensorBoard.\n\n    Parameters:\n        writer (tensorboard.SummaryWriter): TensorBoard SummaryWriter instance.\n        step (int): Counter usually specifying steps/epochs/time.\n        matrix (numpy.array): Square-shaped array of size class x class.\n            Should specify cross-class accuracies/confusion in percent\n            values (range 0-1).\n        class_dict (dict): Dictionary specifying class names as keys and\n            corresponding integer labels/targets as values.\n        save_path (str): Path used for saving\n    '
    all_categories = sorted(class_dict, key=class_dict.get)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax, boundaries=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    ax.set_xticklabels(([''] + all_categories), rotation=90)
    ax.set_yticklabels(([''] + all_categories))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(False)
    plt.tight_layout()
    writer.add_figure('Training data', fig, global_step=str(step))
    plt.savefig(os.path.join(save_path, (('confusion_epoch_' + str(step)) + '.png')), bbox_inches='tight')

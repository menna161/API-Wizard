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


def visualize_means(means, classes_order, data_name, save_path, name):
    '\n    Visualization of means, e.g. of latent code z.\n\n    Parameters:\n        means (torch.Tensor): 2-D Tensor with one mean z vector per class.\n        classes_order (dict): Defines mapping between integer indices and class names (strings).\n        data_name (str): Dataset name. Used for naming.\n        save_path (str): Saving path.\n        name (str): Name for type of mean, e.g. "z".\n    '
    classes_order = sorted(classes_order)
    classes = []
    for key in classes_order:
        classes.append(key)
    plt.figure(figsize=(20, 20))
    ax = sns.heatmap(means.cpu().numpy(), cmap='BrBG')
    ax.set_title(data_name, fontsize=title_font_size)
    ax.set_xlabel((name + ' mean activations'), fontsize=axes_font_size)
    ax.set_yticklabels(classes, rotation=0)
    plt.savefig(os.path.join(save_path, (name + '_mean_activations.png')), bbox_inches='tight')

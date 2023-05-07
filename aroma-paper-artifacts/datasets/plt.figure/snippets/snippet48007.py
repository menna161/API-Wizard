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


def visualize_weibull_outlier_probabilities(data_outlier_probs, other_data_outlier_probs_dict, data_name, save_path, tailsize):
    "\n    Visualization of Weibull CDF outlier probabilites.\n\n    Parameters:\n        data_outlier_probs (np.array): Outlier probabilities for each input of the trained dataset's validation set.\n        other_data_outlier_probs_dict (dictionary): Outlier probabilities for each input of an unseen dataset.\n        data_name (str): Original trained dataset's name.\n        save_path (str): Saving path.\n        tailsize (int): Fitted Weibull model's tailsize.\n    "
    data_outlier_probs = np.concatenate(data_outlier_probs, axis=0)
    data_weights = (np.ones_like(data_outlier_probs) / float(len(data_outlier_probs)))
    plt.figure(figsize=(20, 20))
    plt.hist(data_outlier_probs, label=data_name, weights=data_weights, bins=50, color=colors[0], alpha=1.0, edgecolor='white', linewidth=5)
    c = 0
    for (other_data_name, other_data_outlier_probs) in other_data_outlier_probs_dict.items():
        other_data_outlier_probs = np.concatenate(other_data_outlier_probs, axis=0)
        other_data_weights = (np.ones_like(other_data_outlier_probs) / float(len(other_data_outlier_probs)))
        plt.hist(other_data_outlier_probs, label=other_data_name, weights=other_data_weights, bins=50, color=colors[c], alpha=0.5, edgecolor='white', linewidth=5)
        c += 1
    plt.title(('Outlier probabilities: tailsize ' + str(tailsize)), fontsize=title_font_size)
    plt.xlabel('Outlier probability according to Weibull CDF', fontsize=axes_font_size)
    plt.ylabel('Percentage', fontsize=axes_font_size)
    plt.xlim(left=(- 0.05), right=1.05)
    plt.ylim(bottom=(- 0.05), top=1.05)
    plt.legend(loc=0)
    plt.savefig(os.path.join(save_path, (((((data_name + '_') + ','.join(list(other_data_outlier_probs_dict.keys()))) + '_weibull_outlier_probabilities_tailsize_') + str(tailsize)) + '.png')), bbox_inches='tight')

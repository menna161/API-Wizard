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


def visualize_entropy_classification(data, other_data_dicts, dict_key, data_name, thresholds, save_path):
    "\n    Visualization of percentage of datasets considered as statistical outliers evaluated for different\n    entropy thresholds.\n\n    Parameters:\n        data (list): Dataset outlier percentages per rejection prior value for the trained dataset's validation set.\n        other_data_dicts (dictionary of dictionaries):\n            Dataset outlier percentages per rejection prior value for an unseen dataset.\n        dict_key (str): Dictionary key of the values to visualize\n        data_name (str): Original trained dataset's name.\n        thresholds (list): List of integers with rejection prior values.\n        save_path (str): Saving path.\n    "
    lw = 10
    plt.figure(figsize=(20, 20))
    plt.plot(thresholds, data, label=data_name, color=colors[0], linestyle='solid', linewidth=lw)
    c = 0
    for (other_data_name, other_data_dict) in other_data_dicts.items():
        plt.plot(thresholds, other_data_dict[dict_key], label=other_data_name, color=colors[c], linestyle=linestyles[(c % len(linestyles))], linewidth=lw)
        c += 1
    plt.xlabel('Predictive entropy', fontsize=axes_font_size)
    plt.ylabel('Percentage of dataset outliers', fontsize=axes_font_size)
    plt.xlim(left=(- 0.05), right=thresholds[(- 1)])
    plt.ylim(bottom=(- 0.05), top=1.05)
    plt.legend(loc=0, fontsize=(legend_font_size - 15))
    plt.savefig(os.path.join(save_path, ((((data_name + '_') + ','.join(list(other_data_dicts.keys()))) + '_entropy_outlier_classification') + '.pdf')), bbox_inches='tight')

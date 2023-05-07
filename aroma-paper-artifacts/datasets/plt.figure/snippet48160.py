import torch
import os
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def visualize_classification_scores(data, other_data_dicts, dict_key, data_name, save_path):
    "\n    Visualization of classification scores per dataset.\n\n    Parameters:\n        data (list): Classification scores.\n        other_data_dicts (dictionary of dictionaries): Dictionary of key-value pairs per dataset\n        dict_key (string): Dictionary key to plot\n        data_name (str): Original trained dataset's name.\n        save_path (str): Saving path.\n    "
    data = [y for x in data for y in x]
    plt.figure(figsize=(20, 20))
    plt.hist(data, label=data_name, alpha=1.0, bins=20, color=colors[0])
    c = 0
    for (other_data_name, other_data_dict) in other_data_dicts.items():
        other_data = [y for x in other_data_dict[dict_key] for y in x]
        plt.hist(other_data, label=other_data_name, alpha=0.5, bins=20, color=colors[c])
        c += 1
    plt.title('Dataset classification', fontsize=title_font_size)
    plt.xlabel('Classification confidence', fontsize=axes_font_size)
    plt.ylabel('Number of images', fontsize=axes_font_size)
    plt.legend(loc=0)
    plt.xlim(left=(- 0.0), right=1.05)
    plt.savefig(os.path.join(save_path, (((data_name + '_') + ','.join(list(other_data_dicts.keys()))) + '_classification_scores.png')), bbox_inches='tight')

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


def visualize_recon_loss_histogram(data, other_data_dicts, max_recon_loss, dict_key, data_name, save_path):
    "\n    Visualization of the entropy the datasets.\n\n    Parameters:\n        data (list):\n        other_data_dicts (dictionary of dictionaries): Dictionary of key-value pairs per dataset\n        dict_key (str): Dictionary key to plot\n        data_name (str): Original trained dataset's name.\n        save_path (str): Saving path.\n    "
    data = [x for x in data]
    plt.figure(figsize=(20, 20))
    plt.hist(data, label=data_name, alpha=1.0, bins=25, color=colors[0])
    c = 0
    for (other_data_name, other_data_dict) in other_data_dicts.items():
        other_data = [x for x in other_data_dict[dict_key]]
        plt.hist(other_data, label=other_data_name, alpha=0.5, bins=25, color=colors[c])
        c += 1
    plt.title('Dataset reconstruction', fontsize=title_font_size)
    plt.xlabel('Reconstruction loss (nats)', fontsize=axes_font_size)
    plt.ylabel('Number of images', fontsize=axes_font_size)
    plt.legend(loc=0)
    plt.xlim(left=(- 0.0), right=max_recon_loss)
    plt.savefig(os.path.join(save_path, (((data_name + '_') + ','.join(list(other_data_dicts.keys()))) + '_reconstruction_losses.png')), bbox_inches='tight')

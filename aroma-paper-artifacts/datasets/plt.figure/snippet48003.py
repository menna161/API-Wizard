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


def visualize_classification_uncertainty(data_mus, data_sigmas, other_data_dicts, other_data_mu_key, other_data_sigma_key, data_name, num_samples, save_path):
    "\n    Visualization of prediction uncertainty computed over multiple samples for each input.\n\n    Parameters:\n        data_mus (list or torch.Tensor): Encoded mu values for trained dataset's validation set.\n        data_sigmas (list or torch.Tensor): Encoded sigma values for trained dataset's validation set.\n        other_data_dicts (dictionary of dictionaries): A dataset with values per dictionary, among them mus and sigmas\n        other_data_mu_key (str): Dictionary key for the mus\n        other_data_sigma_key (str): Dictionary key for the sigmas\n        data_name (str): Original dataset's name.\n        num_samples (int): Number of used samples to obtain prediction values.\n        save_path (str): Saving path.\n    "
    data_mus = [y for x in data_mus for y in x]
    data_sigmas = [y for x in data_sigmas for y in x]
    plt.figure(figsize=(20, 14))
    plt.scatter(data_mus, data_sigmas, label=data_name, s=75, c=colors[0], alpha=1.0)
    c = 0
    for (other_data_name, other_data_dict) in other_data_dicts.items():
        other_data_mus = [y for x in other_data_dict[other_data_mu_key] for y in x]
        other_data_sigmas = [y for x in other_data_dict[other_data_sigma_key] for y in x]
        plt.scatter(other_data_mus, other_data_sigmas, label=other_data_name, s=75, c=colors[c], alpha=0.3, marker='*')
        c += 1
    plt.xlabel('Prediction mean', fontsize=axes_font_size)
    plt.ylabel('Prediction standard deviation', fontsize=axes_font_size)
    plt.xlim(left=(- 0.05), right=1.05)
    plt.ylim(bottom=(- 0.05), top=0.55)
    plt.legend(loc=1, fontsize=legend_font_size)
    plt.savefig(os.path.join(save_path, (((((data_name + '_vs_') + ','.join(list(other_data_dicts.keys()))) + '_classification_uncertainty_') + str(num_samples)) + '_samples.pdf')), bbox_inches='tight')

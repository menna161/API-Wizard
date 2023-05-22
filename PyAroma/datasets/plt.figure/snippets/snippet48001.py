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


def visualize_dataset_in_2d_embedding(writer, encoding_list, dataset_name, save_path, task=1):
    '\n    Visualization of 2-D latent embedding. Is saved to both hard-disc as well as TensorBoard.\n\n    Parameters:\n        writer (tensorboard.SummaryWriter): TensorBoard SummaryWriter instance.\n        encoding_list (list): List of Tensors containing encoding values\n        dataset_name (str): Dataset name.\n        save_path (str): Path used for saving.\n        task (int): task counter. Used for naming.\n    '
    num_classes = len(encoding_list)
    encoded_classes = []
    for i in range(len(encoding_list)):
        if isinstance(encoding_list[i], torch.Tensor):
            encoded_classes.append(([i] * encoding_list[i].size(0)))
        else:
            device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
            encoding_list[i] = torch.Tensor(encoding_list[i]).to(device)
            encoded_classes.append(([i] * 0))
    encoded_classes = np.concatenate(np.asarray(encoded_classes), axis=0)
    encoding = torch.cat(encoding_list, dim=0)
    if (encoding.size(1) != 2):
        print('Skipping visualization of latent space because it is not 2-D')
        return
    encoded_dim1 = np.squeeze(encoding.narrow(1, 0, 1).cpu().numpy())
    encoded_dim2 = np.squeeze(encoding.narrow(1, 1, 1).cpu().numpy())
    xlabel = 'z dimension 1'
    ylabel = 'z dimension 2'
    my_cmap = ListedColormap(sns.color_palette('Paired', num_classes).as_hex())
    fig = plt.figure(figsize=(20, 20))
    plt.scatter(encoded_dim1, encoded_dim2, c=encoded_classes, cmap=my_cmap)
    plt.xlabel(xlabel, fontsize=axes_font_size)
    plt.ylabel(ylabel, fontsize=axes_font_size)
    plt.xticks(fontsize=ticks_font_size)
    plt.yticks(fontsize=ticks_font_size)
    cbar = plt.colorbar(ticks=np.linspace(0, (num_classes - 1), num_classes))
    cbar.ax.set_yticklabels([str(i) for i in range(num_classes)])
    cbar.ax.tick_params(labelsize=legend_font_size)
    plt.tight_layout()
    writer.add_figure('latent_embedding', fig, global_step=task)
    plt.savefig(os.path.join(save_path, (((dataset_name + '_latent_2d_embedding_task_') + str(task)) + '.png')), bbox_inches='tight')

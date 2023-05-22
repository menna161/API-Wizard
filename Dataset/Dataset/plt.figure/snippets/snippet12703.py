import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_alignment(alignment, path, title=None, split_title=False, max_len=None):
    if (max_len is not None):
        alignment = alignment[(:, :max_len)]
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    im = ax.imshow(alignment, aspect='auto', origin='lower', interpolation='none')
    fig.colorbar(im, ax=ax)
    xlabel = 'Decoder timestep'
    if split_title:
        title = split_title_line(title)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.ylabel('Encoder timestep')
    plt.tight_layout()
    plt.savefig(path, format='png')
    plt.close()

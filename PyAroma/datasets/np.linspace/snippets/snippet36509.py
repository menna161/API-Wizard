import numpy as np
import matplotlib.cm as cm
from math import ceil, sqrt


def plot_single_patch(ax, patch, x=3, y=3, positive=True, average=False):
    if (not positive):
        patch -= patch.mean(axis=(0, 1))[(np.newaxis, np.newaxis, :)]
    n_channel = (x * y)
    patch = patch.copy()
    std = np.sqrt((patch ** 2).sum(axis=(0, 1)))
    std[(std == 0)] = 0
    patch /= std[(np.newaxis, np.newaxis, :)]
    channel_step = (patch.shape[2] // n_channel)
    if average:
        patch = np.concatenate([np.sum(patch[(:, :, (i * channel_step):((i + 1) * channel_step))], axis=2)[(..., np.newaxis)] for i in range(n_channel)], axis=2)
    patch = patch[(:, :, np.linspace(0, (patch.shape[2] - 1), n_channel).astype('int'))]
    squares_patch = np.zeros(((x * patch.shape[0]), (y * patch.shape[1])))
    idx = 0
    for i in range(x):
        for j in range(y):
            if (idx < patch.shape[2]):
                squares_patch[((i * patch.shape[0]):((i + 1) * patch.shape[0]), (j * patch.shape[1]):((j + 1) * patch.shape[1]))] = patch[(:, :, idx)]
                idx += 1
    ax.imshow(squares_patch, interpolation='nearest')
    for j in range(1, y):
        ax.axvline((j * patch.shape[1]), c='white', linewidth=1)
    for i in range(1, x):
        ax.axhline(((i * patch.shape[0]) - 1), c='white', linewidth=1)
    ax.set_xticks(())
    ax.set_yticks(())
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    return ax

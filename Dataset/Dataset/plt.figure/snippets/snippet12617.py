import matplotlib.pyplot as plt
import time
import numpy as np
import sys


def save_spectrogram(M, path, length=None):
    M = np.flip(M, axis=0)
    if length:
        M = M[(:, :length)]
    fig = plt.figure(figsize=(12, 6))
    plt.imshow(M, interpolation='nearest', aspect='auto')
    fig.savefig(f'{path}.png', bbox_inches='tight')
    plt.close(fig)

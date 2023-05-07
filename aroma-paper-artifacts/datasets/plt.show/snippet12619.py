import matplotlib.pyplot as plt
import time
import numpy as np
import sys


def plot_spec(M):
    M = np.flip(M, axis=0)
    plt.figure(figsize=(18, 4))
    plt.imshow(M, interpolation='nearest', aspect='auto')
    plt.show()

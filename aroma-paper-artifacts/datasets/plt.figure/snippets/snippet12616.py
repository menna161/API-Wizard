import matplotlib.pyplot as plt
import time
import numpy as np
import sys


def save_attention(attn, path):
    fig = plt.figure(figsize=(12, 6))
    plt.imshow(attn.T, interpolation='nearest', aspect='auto')
    fig.savefig(f'{path}.png', bbox_inches='tight')
    plt.close(fig)

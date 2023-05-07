import sys
import argparse
import numpy as np
import h5py
import argparse
from PIL import Image
import matplotlib.pyplot as plt
import math
import time
import os
from collections import deque
import seaborn as sns
from screen_manager import ScreenManager


def figure_plot(steer_pred1, steer_pred2, steer_gt, iteration):
    (fig, ax) = plt.subplots(figsize=(16, 7))
    time_vec = range(0, len(steer_pred1))
    time_vec = [((float(x) / 10.0) + 200) for x in time_vec]
    ax.plot(time_vec, steer_pred1, 'g', label='Model 2')
    ax.plot(time_vec, steer_pred2, 'r', label='Model 1')
    ax.plot(time_vec, steer_gt, 'b', label='Ground Truth')
    ax.set_ylim([(- 0.6), 0.8])
    ax.set_xlim([200, 650])
    for item in (([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels()) + ax.get_yticklabels()):
        item.set_fontsize(24)
    ax.legend(loc='upper center', ncol=3)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Steering Value (radians)')
    fig.savefig((('footage_offline/plot' + str(iteration)) + '.png'), orientation='landscape', bbox_inches='tight')
    plt.close(fig)

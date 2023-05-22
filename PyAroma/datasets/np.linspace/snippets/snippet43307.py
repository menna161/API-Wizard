from matplotlib import pyplot as plt
import numpy as np
import torch
import os
import yaml
import math
import argparse


def plot_env_baseline(ax, env):
    x = np.linspace(0.0, 2.0, num=100)
    (mean, std) = BASELINE[env]
    std_err = (std / np.sqrt(5))
    mean = np.repeat(mean, 100)
    std_err = np.repeat(std_err, 100)
    ax.plot(x, mean, 'k', label='Dataset')
    ax.fill_between(x, (mean - std_err), (mean + std_err), color='k', alpha=0.1)

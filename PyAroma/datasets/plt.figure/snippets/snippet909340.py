import matplotlib.pyplot as plt
from pylab import *
import tensorflow as tf
import numpy as np
import random
import time
import pickle
import pdb


def save_plot_figure(performance_list, name='performance.jpg'):
    plt.figure()
    plot(performance_list)
    plt.title('Performance')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.savefig(name)

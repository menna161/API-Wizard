import matplotlib.pyplot as plt
from pylab import *
import tensorflow as tf
import numpy as np
import random
import time
import pickle
import pdb


def plot_data(path):
    plt.figure()
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if (line[0] in '0123456789'):
                num_list = [float(x) for x in line.split()]
                plot(num_list)
                plt.title('Performance')
                plt.xlabel('Epoch')
                plt.ylabel('Accuracy')
                plt.savefig(path.replace('.txt', '.jpg'))
            else:
                continue

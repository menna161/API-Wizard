import networkx as nx
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll
import collections
from .state import State
from .substitution_system import SubstitutionSystem
import cPickle as pickle
import pickle


def plot_degree_distribution(network, xlabel='Node degree', ylabel_freq='Frequency', ylabel_prob='Probability', in_degree=False, out_degree=False, equation=None, equation_x=0.51, equation_y=0.76, equation_text='', equation_color='r', color='r', title=None):
    "\n    Create a node degree distribution plot for the given network.\n\n    :param network: A Netomaton Network instance.\n\n    :param xlabel: The x-axis label.\n\n    :param ylabel_freq: The frequency y-axis label.\n\n    :param ylabel_prob: The probability y-axis label.\n\n    :param in_degree: If True, the in-degree will be used. (default is False)\n\n    :param out_degree: If True, the out-degree will be used. (default is False)\n\n    :param equation: A callable that computes the degree distribution, given a node degree.\n\n    :param equation_x: The equation's x coordinate.\n\n    :param equation_y: The equation's y coordinate.\n\n    :param equation_text: The equation to display.\n\n    :param equation_color: The equation text's color. It must be a valid Matplotlib color.\n\n    :param color: The color to use for the plot. It must be a valid Matplotlib color.\n\n    :param title: The plot's title.\n    "
    degree_counts = {}
    for node in network.nodes:
        if in_degree:
            degree = network.in_degree(node)
        elif out_degree:
            degree = network.out_degree(node)
        else:
            degree = network.degree(node)
        if (degree not in degree_counts):
            degree_counts[degree] = 0
        degree_counts[degree] += 1
    x = [i for i in range(1, (max(degree_counts) + 1))]
    height = [(degree_counts[i] if (i in degree_counts) else 0) for i in x]
    plt.bar(x, height)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel_freq)
    if equation:
        y = [equation(k) for k in x]
        plt.twinx()
        plt.plot(x, y, color=color)
        plt.ylabel(ylabel_prob)
        plt.text(equation_x, equation_y, equation_text, transform=plt.gca().transAxes, color=equation_color)
    if title:
        plt.title(title)
    plt.show()

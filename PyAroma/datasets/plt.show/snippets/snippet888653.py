import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import *
import ipywidgets as widgets
import whynot as wn
from whynot.dynamics import DynamicsExperiment
from whynot.simulators import opioid
from whynot.simulators.opioid.experiments import sample_initial_states, opioid_intervention, overdose_deaths
from whynot_estimators import causal_forest
from matplotlib import rc


def plot_relative_error(data_dir='heterogeneous_example_data'):
    if (data_dir[(- 1)] != '/'):
        data_dir += '/'
    data_filename = (data_dir + 'heterogeneous_example_error_data.json')
    data = json.load(open(data_filename))
    plotting_data = []
    for n in data.keys():
        for i in data[n].keys():
            d = {'Sample Size': int(n), 'Iteration': int(i)}
            true_effects = data[n][str(i)]['true_effects']
            estimated_effects = data[n][str(i)]['estimated_effects']
            error = (np.array(true_effects) - np.array(estimated_effects))
            relative_error = (np.linalg.norm(error) / np.linalg.norm(true_effects))
            d['Relative Error'] = relative_error
            plotting_data.append(d)
    plotting_df = pd.DataFrame(plotting_data)
    plt.figure(figsize=(18, 8))
    ax = plt.gca()
    grid = sns.lineplot(x='Sample Size', y='Relative Error', data=plotting_df, marker='o', ax=ax)
    sample_sizes = [int(n) for n in data.keys()]
    ax.set_xticks(sample_sizes)
    ax.set_xticklabels(([''] + sample_sizes[1:]), rotation=45)
    ax.set_xlim([0, (max(sample_sizes) + 100)])
    sns.despine()
    plt.title('Relative Error of Causal Forest')
    plt.show()

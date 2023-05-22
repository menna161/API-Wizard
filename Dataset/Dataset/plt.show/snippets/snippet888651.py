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


def effects_histogram(true_effects, estimated_effects=None, num_bins=100, title=None, x_range=None, y_max=None, show_avg=True):
    plt.figure(figsize=(18, 8))
    if (title is None):
        if (estimated_effects is None):
            title = 'True Heterogeneous Effects'
        else:
            title = 'True and Estimated Heterogeneous Effects'
    plt.title(title, pad=20)
    if ((estimated_effects is not None) and (x_range is None)):
        x_range = np.percentile(np.concatenate((true_effects, estimated_effects)), (5, 95))
    true_effects_mean = np.mean(true_effects)
    plt.axvline(x=true_effects_mean, color='C0', linestyle='--')
    plt.hist(true_effects, bins=num_bins, range=x_range, density=True, alpha=0.5, color='C0', label='True Effects')
    if (estimated_effects is not None):
        estimated_effects_mean = np.mean(estimated_effects)
        plt.axvline(x=estimated_effects_mean, color='C1', linestyle='--')
        plt.hist(estimated_effects, bins=num_bins, range=x_range, density=True, alpha=0.5, color='C1', label='Estimated Effects')
    if y_max:
        plt.ylim(top=(y_max * 1.05))
    if show_avg:
        plt.text(true_effects_mean, (plt.ylim()[1] * 0.95), '  True ATE', color='C0', fontsize=18)
        if (estimated_effects is not None):
            plt.text(estimated_effects_mean, (plt.ylim()[1] * 0.9), '  Estimated ATE', color='C1', fontsize=18)
    plt.xlabel('Effect Size')
    plt.ylabel('Density')
    plt.legend(fontsize=18)
    plt.show()

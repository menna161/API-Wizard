import dataclasses
from dataclasses import dataclass
import json
from pathlib import Path
import numpy as np
import pandas as pd
from axcell.models.structure.nbsvm import *
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
import seaborn as sn
from enum import Enum
import pickle


def _plot_confusion_matrix(self, cm, normalize, fmt=None):
    if normalize:
        s = cm.sum(axis=1)[(:, None)]
        s[(s == 0)] = 1
        cm = (cm / s)
    if (fmt is None):
        fmt = ('0.2f' if normalize else 'd')
    target_names = self.get_cm_labels(cm)
    df_cm = pd.DataFrame(cm, index=[i for i in target_names], columns=[i for i in target_names])
    plt.figure(figsize=(10, 10))
    ax = sn.heatmap(df_cm, annot=True, square=True, fmt=fmt, cmap='YlGnBu', mask=(cm == 0), linecolor='black', linewidths=0.01)
    ax.set_ylabel('True')
    ax.set_xlabel('Predicted')

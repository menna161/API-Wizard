from fastai.text import *
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from IPython.display import HTML, display


def plot_confusion_matrix(self, name):
    (cm, target_names) = self.confusion_matrix(name)
    df_cm = pd.DataFrame(cm, index=[i for i in target_names], columns=[i for i in target_names])
    plt.figure(figsize=(20, 20))
    ax = sn.heatmap(df_cm, annot=True, square=True, fmt='d', cmap='YlGnBu', mask=(cm == 0), linecolor='black', linewidths=0.01)
    ax.set_ylabel('True')
    ax.set_xlabel('Predicted')

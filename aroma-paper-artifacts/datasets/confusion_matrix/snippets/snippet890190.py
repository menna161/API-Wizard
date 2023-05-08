from fastai.text import *
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from IPython.display import HTML, display


def confusion_matrix(self, name):
    pred_y = np.array(self.df[f'{name}_pred'])
    true_y = np.array(self.df[f'{name}_gold'])
    labels = list(sorted(set((list(true_y) + list(pred_y)))))
    cm = confusion_matrix(true_y, pred_y, labels)
    return (cm, labels)

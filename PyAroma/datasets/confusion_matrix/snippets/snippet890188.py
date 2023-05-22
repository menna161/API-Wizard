from fastai.text import *
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from IPython.display import HTML, display


def calc_metric(self, metric_name, metric_fn, *col_names, best_only=True):
    prefix = ('best_' if best_only else '')
    result = {f'{prefix}{metric_name}_{col}': metric_fn(self.binary_confusion_matrix(col, best_only=best_only)) for col in col_names}
    if (len(col_names) > 1):
        cm = self.binary_confusion_matrix(*col_names, best_only=best_only)
        result[f'{prefix}{metric_name}_all'] = metric_fn(cm)
        result[f'{prefix}TP_all'] = cm.tp
        result[f'{prefix}FP_all'] = cm.fp
        relevant_gold = self.df['model_type_gold'].str.contains('model-best')
        if best_only:
            relevant_pred = self.df['model_type_pred'].str.contains('model-best')
        else:
            relevant_pred = relevant_gold
        result[f'{prefix}count'] = (relevant_pred | relevant_gold).sum()
    return result

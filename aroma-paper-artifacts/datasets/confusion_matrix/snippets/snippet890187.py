from fastai.text import *
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from IPython.display import HTML, display


def binary_confusion_matrix(self, *col_names, best_only=True):
    relevant_gold = self.df['model_type_gold'].str.contains('model-best')
    if best_only:
        relevant_pred = self.df['model_type_pred'].str.contains('model-best')
    else:
        relevant_pred = relevant_gold
    pred_positive = relevant_pred
    gold_positive = relevant_gold
    equal = self.matching(*col_names)
    if self.topk_metrics:
        equal = pd.Series(equal, index=pred_positive.index).groupby('cell_ext_id').max()
        pred_positive = pred_positive.groupby('cell_ext_id').head(1)
        gold_positive = gold_positive.groupby('cell_ext_id').head(1)
    tp = ((equal & pred_positive) & gold_positive).sum()
    tn = ((equal & (~ pred_positive)) & (~ gold_positive)).sum()
    fp = (pred_positive & ((~ equal) | (~ gold_positive))).sum()
    fn = (gold_positive & ((~ equal) | (~ pred_positive))).sum()
    return CM(tp=tp, tn=tn, fp=fp, fn=fn)

from functools import partial
from .experiment import Experiment, label_map_ext
from axcell.models.structure.nbsvm import *
from sklearn.metrics import confusion_matrix
from .nbsvm import preds_for_cell_content, preds_for_cell_content_max, preds_for_cell_content_multi
import dataclasses
from dataclasses import dataclass
from typing import Tuple
from axcell.helpers.training import set_seed
from fastai.text import *
from fastai.text.learner import _model_meta
import torch
import numpy as np
from pathlib import Path
import json


def _set_results(self, prefix, preds, true_y, true_y_ext=None):

    def metrics(preds, true_y):
        y = true_y
        p = preds
        if self.distinguish_ablation:
            g = {0: 0, 1: 0, 2: 1}.get
            bin_y = np.array([g(x) for x in y])
            bin_p = np.array([g(x) for x in p])
            irr = 2
        else:
            bin_y = y
            bin_p = p
            irr = 1
        acc = (p == y).mean()
        tp = ((y != irr) & (p == y)).sum()
        fp = ((p != irr) & (p != y)).sum()
        fn = ((y != irr) & (p == irr)).sum()
        bin_acc = (bin_p == bin_y).mean()
        bin_tp = ((bin_y != 1) & (bin_p == bin_y)).sum()
        bin_fp = ((bin_p != 1) & (bin_p != bin_y)).sum()
        bin_fn = ((bin_y != 1) & (bin_p == 1)).sum()
        prec = (tp / (fp + tp))
        reca = (tp / (fn + tp))
        bin_prec = (bin_tp / (bin_fp + bin_tp))
        bin_reca = (bin_tp / (bin_fn + bin_tp))
        return {'precision': prec, 'accuracy': acc, 'recall': reca, 'TP': tp, 'FP': fp, 'bin_precision': bin_prec, 'bin_accuracy': bin_acc, 'bin_recall': bin_reca, 'bin_TP': bin_tp, 'bin_FP': bin_fp}
    m = metrics(preds, true_y)
    r = {}
    r[f'{prefix}_accuracy'] = m['accuracy']
    r[f'{prefix}_precision'] = m['precision']
    r[f'{prefix}_recall'] = m['recall']
    r[f'{prefix}_bin_accuracy'] = m['bin_accuracy']
    r[f'{prefix}_bin_precision'] = m['bin_precision']
    r[f'{prefix}_bin_recall'] = m['bin_recall']
    r[f'{prefix}_cm'] = confusion_matrix(true_y, preds).tolist()
    self.update_results(**r)

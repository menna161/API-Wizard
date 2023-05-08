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


def _set_results(self, prefix, preds, true_y, true_y_ext=None):
    m = metrics(preds, true_y)
    r = {}
    r[f'{prefix}_accuracy'] = m['accuracy']
    r[f'{prefix}_precision'] = m['precision']
    r[f'{prefix}_recall'] = m['recall']
    r[f'{prefix}_cm'] = confusion_matrix(true_y, preds, labels=[x.value for x in Labels]).tolist()
    if (true_y_ext is not None):
        r[f'{prefix}_cm_full'] = confusion_matrix(true_y_ext, preds, labels=[x.value for x in LabelsExt]).tolist()
    self.update_results(**r)

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


def show_results(self, *ds, normalize=True, full_cm=True):
    if (not len(ds)):
        ds = ['train', 'valid', 'test']
    for prefix in ds:
        print(f'{prefix} dataset')
        print(f" * accuracy: {self.results[f'{prefix}_accuracy']:.3f}")
        print(f" * μ-precision: {self.results[f'{prefix}_precision']:.3f}")
        print(f" * μ-recall: {self.results[f'{prefix}_recall']:.3f}")
        suffix = ('_full' if (full_cm and (f'{prefix}_cm_full' in self.results)) else '')
        self._plot_confusion_matrix(np.array(self.results[f'{prefix}_cm{suffix}']), normalize=normalize)

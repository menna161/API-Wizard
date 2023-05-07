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


def _transform_df(self, df):
    df = df.copy(True)
    if self.distinguish_ablation:
        df['label'] = 2
        df.loc[(df.ablation, 'label')] = 1
        df.loc[(df.sota, 'label')] = 0
    else:
        df['label'] = 1
        df.loc[(df.sota, 'label')] = 0
        df.loc[(df.ablation, 'label')] = 0
    if self.sigmoid:
        if self.irrelevant_as_class:
            df['irrelevant'] = (~ (df['sota'] | df['ablation']))
        if (not self.distinguish_ablation):
            df['sota'] = (df['sota'] | df['ablation'])
            df = df.drop(columns=['ablation'])
    else:
        df['class'] = df['label']
    drop_columns = []
    if (not self.caption):
        drop_columns.append('caption')
    if (not self.first_column):
        drop_columns.append('col0')
    if (not self.first_row):
        drop_columns.append('row0')
    if (not self.referencing_sections):
        drop_columns.append('sections')
    df = df.drop(columns=drop_columns)
    return df

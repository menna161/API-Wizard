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


def evaluate(self, model, train_df, valid_df, test_df):
    valid_probs = model.get_preds(ds_type=DatasetType.Valid, ordered=True)[0].cpu().numpy()
    test_probs = model.get_preds(ds_type=DatasetType.Test, ordered=True)[0].cpu().numpy()
    train_probs = model.get_preds(ds_type=DatasetType.Train, ordered=True)[0].cpu().numpy()
    self._preds = []
    for (prefix, tdf, probs) in zip(['train', 'valid', 'test'], [train_df, valid_df, test_df], [train_probs, valid_probs, test_probs]):
        preds = np.argmax(probs, axis=1)
        if (self.merge_fragments and (self.merge_type != 'concat')):
            if (self.merge_type == 'vote_maj'):
                vote_results = preds_for_cell_content(tdf, probs)
            elif (self.merge_type == 'vote_avg'):
                vote_results = preds_for_cell_content_multi(tdf, probs)
            elif (self.merge_type == 'vote_max'):
                vote_results = preds_for_cell_content_max(tdf, probs)
            preds = vote_results['pred']
            true_y = vote_results['true']
        else:
            true_y = tdf['label']
            true_y_ext = tdf['cell_type'].apply((lambda x: label_map_ext.get(x, 0)))
        self._set_results(prefix, preds, true_y, true_y_ext)
        self._preds.append(probs)

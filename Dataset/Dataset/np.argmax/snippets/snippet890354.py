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

    def multipreds2preds(preds, threshold=0.5):
        bs = preds.shape[0]
        return np.concatenate([probs, (np.ones((bs, 1)) * threshold)], axis=(- 1)).argmax((- 1))
    for (prefix, tdf, probs) in zip(['train', 'valid', 'test'], [train_df, valid_df, test_df], [train_probs, valid_probs, test_probs]):
        if (self.sigmoid and (not self.irrelevant_as_class)):
            preds = multipreds2preds(probs)
        else:
            preds = np.argmax(probs, axis=1)
        true_y = tdf['label']
        self._set_results(prefix, preds, true_y)
        self._preds.append(probs)

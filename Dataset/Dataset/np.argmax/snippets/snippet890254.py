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


def evaluate(self, model, train_df, valid_df, test_df):
    for (prefix, tdf) in zip(['train', 'valid', 'test'], [train_df, valid_df, test_df]):
        probs = model.predict_proba(tdf['text'])
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

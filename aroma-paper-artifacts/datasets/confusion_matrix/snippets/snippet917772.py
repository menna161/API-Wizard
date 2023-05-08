import collections
import inspect
import json
import hashlib
from datetime import datetime
from multiprocessing.pool import Pool
import numpy as np
import pandas as pd
import SimpleITK as sitk
from nnunet.evaluation.metrics import ConfusionMatrix, ALL_METRICS
from batchgenerators.utilities.file_and_folder_operations import save_json, subfiles, join
from collections import OrderedDict


def evaluate(self, test=None, reference=None, advanced=False, **metric_kwargs):
    'Compute metrics for segmentations.'
    if (test is not None):
        self.set_test(test)
    if (reference is not None):
        self.set_reference(reference)
    if ((self.test is None) or (self.reference is None)):
        raise ValueError('Need both test and reference segmentations.')
    if (self.labels is None):
        self.construct_labels()
    self.metrics.sort()
    _funcs = {m: ALL_METRICS[m] for m in (self.metrics + self.advanced_metrics)}
    frames = inspect.getouterframes(inspect.currentframe())
    for metric in self.metrics:
        for f in frames:
            if (metric in f[0].f_locals):
                _funcs[metric] = f[0].f_locals[metric]
                break
        else:
            if (metric in _funcs):
                continue
            else:
                raise NotImplementedError('Metric {} not implemented.'.format(metric))
    self.result = OrderedDict()
    eval_metrics = self.metrics
    if advanced:
        eval_metrics += self.advanced_metrics
    if isinstance(self.labels, dict):
        for (label, name) in self.labels.items():
            k = str(name)
            self.result[k] = OrderedDict()
            if (not hasattr(label, '__iter__')):
                self.confusion_matrix.set_test((self.test == label))
                self.confusion_matrix.set_reference((self.reference == label))
            else:
                current_test = 0
                current_reference = 0
                for l in label:
                    current_test += (self.test == l)
                    current_reference += (self.reference == l)
                self.confusion_matrix.set_test(current_test)
                self.confusion_matrix.set_reference(current_reference)
            for metric in eval_metrics:
                self.result[k][metric] = _funcs[metric](confusion_matrix=self.confusion_matrix, nan_for_nonexisting=self.nan_for_nonexisting, **metric_kwargs)
    else:
        for (i, l) in enumerate(self.labels):
            k = str(l)
            self.result[k] = OrderedDict()
            self.confusion_matrix.set_test((self.test == l))
            self.confusion_matrix.set_reference((self.reference == l))
            for metric in eval_metrics:
                self.result[k][metric] = _funcs[metric](confusion_matrix=self.confusion_matrix, nan_for_nonexisting=self.nan_for_nonexisting, **metric_kwargs)
    return self.result

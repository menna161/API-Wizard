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


def __init__(self, test=None, reference=None, labels=None, metrics=None, advanced_metrics=None, nan_for_nonexisting=True):
    self.test = None
    self.reference = None
    self.confusion_matrix = ConfusionMatrix()
    self.labels = None
    self.nan_for_nonexisting = nan_for_nonexisting
    self.result = None
    self.metrics = []
    if (metrics is None):
        for m in self.default_metrics:
            self.metrics.append(m)
    else:
        for m in metrics:
            self.metrics.append(m)
    self.advanced_metrics = []
    if (advanced_metrics is None):
        for m in self.default_advanced_metrics:
            self.advanced_metrics.append(m)
    else:
        for m in advanced_metrics:
            self.advanced_metrics.append(m)
    self.set_reference(reference)
    self.set_test(test)
    if (labels is not None):
        self.set_labels(labels)
    elif ((test is not None) and (reference is not None)):
        self.construct_labels()

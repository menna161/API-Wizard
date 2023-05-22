from __future__ import absolute_import
import numpy as np
import chainer
import tqdm
import glob
import warnings
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from ..data import load_image
from .volume import VolumeDataset
from .image import ImageDataset
import pandas as pd
from distutils.version import LooseVersion


def train_valid_split(train, valid_ratio):
    if isinstance(train, BaseDataset):
        valid = train.__copy__()
        n_samples = len(train)
        valid_indices = np.random.choice(np.arange(n_samples), int((valid_ratio * n_samples)), replace=False)
        files = train.files
        for key in files.keys():
            valid._files[key] = np.asarray(files[key])[valid_indices]
            train._files[key] = np.delete(np.asarray(files[key]), valid_indices)
    elif isinstance(train, (list, np.ndarray)):
        valid = np.asarray(train)
        n_samples = len(train)
        valid_indices = np.random.choice(np.arange(n_samples), int((valid_ratio * n_samples)), replace=False)
        valid = valid[valid_indices]
        train = np.delete(train, valid_indices)
    assert ((len(train) + len(valid)) == n_samples)
    return (train, valid)

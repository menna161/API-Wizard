import os, numpy as np
from time import time
import cv2, torch
from torch.utils.data import Dataset
from auxiliary.transforms import get_transform
from scipy.spatial.distance import cdist


def filter_samples(opt, fnames, labels, classes):
    '\n    Select a subset of classes. Mostly for faster debugging.\n    '
    (fnames, labels) = (np.array(fnames), np.array(labels))
    if (opt.train_samples != (- 1)):
        sel = np.linspace(0, (len(fnames) - 1), min(opt.train_samples, len(fnames))).astype(int)
        (fnames, labels) = (fnames[sel], labels[sel])
    return (np.array(fnames), np.array(labels), np.array(classes))

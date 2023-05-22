import os, numpy as np
from time import time
import cv2, torch
from torch.utils.data import Dataset
from auxiliary.transforms import get_transform
from scipy.spatial.distance import cdist


def filter_classes(opt, fnames, labels, classes, class_embedding):
    '\n    Select a subset of classes. Mostly for faster debugging.\n    '
    sel = (np.ones(len(classes)) == 1)
    if (opt.class_total > 0):
        sel = np.linspace(0, (len(classes) - 1), opt.class_total).astype(int)
    classes = np.array(classes)[sel].tolist()
    class_embedding = class_embedding[sel]
    fnames = [f for (i, f) in enumerate(fnames) if (labels[i] in classes)]
    labels = [l for l in labels if (l in classes)]
    return (np.array(fnames), np.array(labels), np.array(classes), class_embedding)

import os
from multiprocessing.pool import Pool
import cv2
import numpy as np
from training.metric import calc_score
import warnings


def calc(f):
    label = cv2.imread(os.path.join(preds_dir, f), cv2.IMREAD_UNCHANGED)
    label_file = (('mask_' + '_'.join(f[:(- 4)].split('_')[(- 2):])) + '.tif')
    gt_label = cv2.imread(os.path.join(labels_dir, label_file), cv2.IMREAD_UNCHANGED)
    res = calc_score(gt_label, label)
    nadir = int(f.split('_')[2].lstrip('nadir'))
    return (nadir, res)

import os
import argparse
import time
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool
from sklearn.metrics import average_precision_score, precision_recall_curve
import sys
import pickle
import load as io
from bbox_utils import compute_iou
import pdb


def compute_ap(precision, recall):
    if np.any(np.isnan(recall)):
        return np.nan
    ap = 0
    for t in np.arange(0, 1.1, 0.1):
        try:
            selected_p = precision[(recall >= t)]
        except:
            ForkedPdb().set_trace()
        if (selected_p.size == 0):
            p = 0
        else:
            p = np.max(selected_p)
        ap += (p / 11.0)
    return ap

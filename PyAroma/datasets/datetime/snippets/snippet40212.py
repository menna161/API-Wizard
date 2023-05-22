import argparse
import math
from datetime import datetime
import numpy as np
import tensorflow as tf
import importlib
import os
import sys
import provider
import tf_util
import pc_util
import dfc_dataset


def get_batch_wdp(dataset, idxs, start_idx, end_idx):
    bsize = (end_idx - start_idx)
    batch_data = np.zeros((bsize, NUM_POINT, len(TRAIN_DATASET.columns)))
    batch_label = np.zeros((bsize, NUM_POINT), dtype=np.int32)
    batch_smpw = np.zeros((bsize, NUM_POINT), dtype=np.float32)
    for i in range(bsize):
        if ((start_idx + i) < len(dataset)):
            (ps, seg, smpw) = dataset[idxs[(i + start_idx)]]
            batch_data[(i, ...)] = ps
            batch_label[(i, :)] = seg
            batch_smpw[(i, :)] = smpw
            dropout_ratio = (np.random.random() * 0.875)
            drop_idx = np.where((np.random.random(ps.shape[0]) <= dropout_ratio))[0]
            batch_data[(i, drop_idx, :)] = batch_data[(i, 0, :)]
            batch_label[(i, drop_idx)] = batch_label[(i, 0)]
            batch_smpw[(i, drop_idx)] *= 0
    return (batch_data, batch_label, batch_smpw)
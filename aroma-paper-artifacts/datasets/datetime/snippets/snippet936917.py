import torch
import cv2
import os
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from network.utils import bbox_iou
from datetime import datetime
import multiprocessing
from scipy.optimize import linear_sum_assignment


def track_complete(track, gap_threshold=8):
    max_fid = int(np.max(track[(:, 0)]))
    min_fid = int(np.min(track[(:, 0)]))
    ips = []
    ip_cnt = 0
    max_missing_len = 0
    for (i, fid) in enumerate(list(track[(:(- 1), 0)])):
        if ((track[((i + 1), 0)] - 1) != track[(i, 0)]):
            if (((track[((i + 1), 0)] - track[(i, 0)]) - 1) > gap_threshold):
                continue
            cur_fid = (track[(i, 0)] + 1)
            missing_len = 0
            while (cur_fid < track[((i + 1), 0)]):
                ips.append(ip_linear(track[(i + 1)], track[i], cur_fid))
                cur_fid = (cur_fid + 1)
                missing_len = (missing_len + 1)
            ip_cnt = (ip_cnt + missing_len)
            max_missing_len = max(max_missing_len, missing_len)
    assert (len(ips) == ip_cnt), (track, ips)
    ips.append(track)
    new_track = np.concatenate(ips, axis=0)
    new_track = new_track[new_track[(:, 0)].argsort()]
    if (ip_cnt == 0):
        return (track, 0)
    else:
        return (new_track, ip_cnt)

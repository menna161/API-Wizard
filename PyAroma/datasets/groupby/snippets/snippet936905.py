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


def filt_bbox(save_path):

    def bboxfilt(res, l=8):
        max_frame = np.max(res[0])
        range_mask = (((res[6] >= l) | (res[0] <= 8)) | ((res[0] + 8) >= max_frame))
        return res[range_mask]

    def trackfilt(track, l=16):
        max_fid = int(np.max(track[0]))
        min_fid = int(np.min(track[0]))
        return ((max_fid - min_fid) < 5)

    def ip_linear(det1, det2, fid):
        fid1 = det1[0]
        fid2 = det2[0]
        w1 = ((1.0 * (fid2 - fid)) / (fid2 - fid1))
        w2 = ((1.0 * (fid - fid1)) / (fid2 - fid1))
        ip = np.copy(det1)
        ip[0] = fid
        ip[2:6] = ((w1 * det1[2:6]) + (w2 * det2[2:6]))
        return np.array([ip])

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
    param_pairs = [(['-05-'], [0, 4, 8]), (['-10-'], [0, 6, 8]), (['-11-'], [0, 6, 8]), (['-13-'], [0, 9, 8]), (['-02-'], [0, 6, 8]), (['-09-'], [0, 4, 8]), (['-04-'], [0, 12, 8]), (['-06-'], [0, 4, 8]), (['-07-'], [0, 6, 8]), (['-12-'], [0, 6, 8]), (['-14-'], [0, 9, 8]), (['-01-'], [0, 6, 30]), (['-08-'], [0, 4, 30]), (['-03-'], [0, 12, 30])]
    params = {}
    for (file_nums, param) in param_pairs:
        params.update({x: param for x in file_nums})
    file_num = None
    for k in params.keys():
        if ((k in save_path) and (file_num is None)):
            file_num = k
        elif (k in save_path):
            assert False
    res = pd.read_csv(save_path, header=None)
    if (file_num is not None):
        min_num = params[file_num][0]
        min_bbox = params[file_num][1]
        res = bboxfilt(res, min_bbox)
        filtered_tracks = [x[0] for x in res.groupby(1) if trackfilt(x[1], min_num)]
        inds = [(res.iloc[(x, 1)] not in filtered_tracks) for x in range(len(res))]
        res = res[inds]
        inds = np.unique(res[1])
        dict_map = {x: (i + 1) for (i, x) in enumerate(inds)}
        res[1] = res[1].map((lambda x: dict_map[x]))
    tracks = res.groupby(1)
    new_tracks = []
    for tid in tracks.groups.keys():
        (res, _) = track_complete(tracks.get_group(tid).values, params[file_num][2])
        if (res is not None):
            new_tracks.append(res)
    new_tracks = np.concatenate(new_tracks)
    new_tracks = new_tracks[new_tracks[(:, 0)].argsort()]
    np.savetxt(save_path, new_tracks, fmt='%i,%i,%f,%f,%f,%f,%i,%f,%i,%i', delimiter=',')

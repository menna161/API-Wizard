import numpy as np
import os
import pandas as pd
from network.utils import bbox_iou
import pickle
from tqdm import tqdm
import argparse
import multiprocessing
from configs.default import __C, cfg_from_file
from dataset.Parsers.structures import *


def get_gt(json_path, frames_path, loose, min_visiblity, height_clamp):
    assert os.path.exists(json_path), 'File does not exist: {}'.format(json_path)
    assert os.path.exists(frames_path), 'Folder does not exist: {}'.format(frames_path)
    split_path = frames_path.split('/')
    if (frames_path[0] == '/'):
        jta_root = ('/' + os.path.join(*split_path[:(- 3)]))
    else:
        jta_root = os.path.join(*split_path[:(- 3)])
    type = split_path[(- 2)]
    video_name = split_path[(- 1)]
    gt_path = os.path.join(jta_root, ((((('gt_' + str(loose)) + '_') + str(min_visiblity)) + '_') + str(height_clamp)), type, video_name)
    try:
        os.makedirs(gt_path)
    except:
        pass
    gt_file = os.path.join(gt_path, 'gt.txt')
    df = pd.read_json(json_path)
    df = df.iloc[(:, [0, 1, 3, 4, 8])]
    df_group = df.groupby([0, 1])

    def get_bbox(g):
        assert (len(g.columns) == 5)
        if (g.iloc[(:, 4)].sum() >= ((1 - min_visiblity) * len(g))):
            return pd.Series([(- 1), 0, 0, 0, 0, 0, 0], dtype=np.int)
        x1 = np.maximum(0, g.iloc[(:, 2)].min())
        y1 = np.maximum(0, g.iloc[(:, 3)].min())
        x2 = np.minimum(1920, g.iloc[(:, 2)].max())
        y2 = np.minimum(1080, g.iloc[(:, 3)].max())
        w = (x2 - x1)
        h = (y2 - y1)
        x1 -= np.round((w * loose))
        y1 -= np.round((h * loose))
        x1 = np.maximum(0.0, x1)
        y1 = np.maximum(0.0, y1)
        w = np.round((w * (1 + (loose * 2))))
        h = np.round((h * (1 + (loose * 2))))
        w = np.minimum((1920 - x1), w)
        h = np.minimum((1080 - y1), h)
        return pd.Series([x1, y1, w, h, 1, 1, 1], dtype=np.int)
    res_df = df_group.apply(get_bbox)
    res_df = res_df[(res_df.iloc[(:, 0)] != (- 1))]
    (ns, edges) = np.histogram(res_df.iloc[(:, 3)], bins=50)
    max_n = np.argmax(ns)
    mode = np.mean(edges[[max_n, (max_n + 1)]])
    res_df = res_df[(res_df.iloc[(:, 3)] > (height_clamp * mode))]
    res_df = res_df[(res_df.iloc[(:, 3)] > 7)]
    res_df.to_csv(gt_file, header=False)

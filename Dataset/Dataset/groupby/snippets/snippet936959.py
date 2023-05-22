import numpy as np
import os
import pandas as pd
from network.utils import bbox_iou
import pickle
from tqdm import tqdm
import shutil
import multiprocessing
from configs.default import __C, cfg_from_file
from dataset.Parsers.structures import *
import argparse


def __init__(self, folder, min_visibility, forward_frames, frame_stride, tube_thre):
    gt_file_path = os.path.join(folder, 'gt/gt.txt')
    self.folder = folder
    self.forward_frames = forward_frames
    self.tube_thre = tube_thre
    self.min_visibility = min_visibility
    self.frame_stride = frame_stride
    gt_file = pd.read_csv(gt_file_path, header=None)
    gt_file = gt_file[(gt_file[6] == 1)]
    gt_file = gt_file[(gt_file[8] > min_visibility)]
    gt_group = gt_file.groupby(0)
    gt_group_keys = gt_group.indices.keys()
    self.max_frame_index = max(gt_group_keys)
    self.tracks = Tracks()
    self.recorder = {}
    for key in gt_group_keys:
        det = gt_group.get_group(key).values
        ids = np.array(det[(:, 1)]).astype(int)
        det = np.array(det[(:, 2:6)])
        det[(:, 2:4)] += det[(:, :2)]
        self.recorder[(key - 1)] = list()
        for (id, d) in zip(ids, det):
            node = Node(d, (key - 1))
            (track_index, node_index) = self.tracks.add_node(node, id)
            self.recorder[(key - 1)].append((track_index, node_index))

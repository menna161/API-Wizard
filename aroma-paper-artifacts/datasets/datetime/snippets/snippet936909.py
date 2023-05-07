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


def matching(tubes, arg, save_path=None, verbose=False, mid_only=True, poi_tubes=None):
    '\n    tubes: All tubes in a video to match. (n, 15 + 1) [mid_frame, mid_box, front_frame, front_box, back_frame, back_box, value]\n    save_path: File path to save formatted result.\n    '
    tracks = []
    if (not isinstance(tubes, np.ndarray)):
        tubes = tubes.cpu().data.numpy()
    if (poi_tubes is not None):
        poi_tubes = adjust_poi_tubes(tubes, poi_tubes)
        tubes = np.concatenate((tubes, poi_tubes))
    tubes = tubes[(- tubes[(:, 15)]).argsort()]
    tubes = tubes[tubes[(:, 0)].argsort(kind='stable')]
    arch_tracks = []
    prev_frame = (- 1)
    tubes_one_frame = 0
    for tube in tubes:
        update_tracks_fast(tracks, tube, arg)
        current_frame = tube[0]
        if ((prev_frame != current_frame) and (prev_frame != (- 1))):
            if verbose:
                print('{}\tFrame: {}\tTubes: {}\tCur tracks:{}\tArch tracks:{}'.format(datetime.now().time(), prev_frame, tubes_one_frame, len(tracks), len(arch_tracks)))
            tubes_one_frame = 0
            if ((int(current_frame) % 10) == 0):
                tracks = archive_tracks(tracks, arch_tracks, current_frame, (arg.forward_frames * arg.frame_stride))
        prev_frame = current_frame
        tubes_one_frame += 1
    arch_tracks.extend(tracks)
    tracks = arch_tracks
    final_processing(tracks, save_path, mid_only)
    return tracks

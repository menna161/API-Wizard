import torch
import cv2
import os
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from network.utils import bbox_iou
from datetime import datetime


def matching(tubes, arg, save_path=None, verbose=False):
    '\n    tubes: All tubes in a video to match. (n, 15 + 1) [mid_frame, mid_box, front_frame, front_box, back_frame, back_box, value]\n    save_path: File path to save formatted result.\n    '
    tracks = []
    if (not isinstance(tubes, np.ndarray)):
        tubes = tubes.cpu().data.numpy()
    tubes = pd.DataFrame(tubes)
    tubes = tubes.astype({0: int, 5: int, 10: int})
    tubes_group = tubes.groupby(0)
    arch_tracks = []
    for frame in sorted(tubes_group.indices.keys()):
        tubes_one_frame = tubes_group.get_group(frame).values
        for tube in tubes_one_frame:
            update_tracks(tracks, tube, arg)
        if verbose:
            print('{}\tFrame: {}\tTubes: {}\tCur tracks:{}\tArch tracks:{}'.format(datetime.now().time(), frame, len(tubes_one_frame), len(tracks), len(arch_tracks)))
        tracks = archive_tracks(tracks, arch_tracks, frame, (arg.forward_frames * arg.frame_stride))
    arch_tracks.extend(tracks)
    tracks = arch_tracks
    final_processing(tracks, save_path)
    return tracks

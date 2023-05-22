import torch
import cv2
import os
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from network.utils import bbox_iou
from datetime import datetime


def final_processing(tracks, save_path):
    res = []
    assert (len(tracks) != 0), ('No Tracks: ' + str(save_path))
    for track in tracks:
        cur_res = np.zeros((len(track.frames), 10))
        for (i, (frame, bbox)) in enumerate(track.frames.items()):
            cur_res[(i, 0)] = (frame + 1)
            cur_res[(i, 2:6)] = (bbox[0] / bbox[1])
            cur_res[(i, 6)] = bbox[1]
            cur_res[(i, 7)] = (bbox[2] / bbox[1])
        cur_res[(:, 1)] = track.id
        res.append(cur_res)
    res = np.concatenate(res)
    res = res[res[(:, 0)].argsort()]
    res[(:, (- 2):)] = (- 1)
    res[(:, 4:6)] -= res[(:, 2:4)]
    if (save_path is not None):
        try:
            if (save_path[0] == '/'):
                os.makedirs(os.path.join('/', *save_path.split('/')[:(- 1)]))
            else:
                os.makedirs(os.path.join(*save_path.split('/')[:(- 1)]))
        except:
            pass
        np.savetxt(save_path, res, fmt='%i,%i,%f,%f,%f,%f,%i,%f,%i,%i', delimiter=',')
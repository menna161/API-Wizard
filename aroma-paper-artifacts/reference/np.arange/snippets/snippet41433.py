import os, numpy as np
from time import time
import cv2, torch
from torch.utils.data import Dataset
from auxiliary.transforms import get_transform
from scipy.spatial.distance import cdist


def load_clips_tsn(fname, clip_len=16, n_clips=1, is_validation=False):
    if (not os.path.exists(fname)):
        print(('Missing: ' + fname))
        return []
    capture = cv2.VideoCapture(fname)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if ((frame_count == 0) or (frame_width == 0) or (frame_height == 0)):
        print('loading error, switching video ...')
        print(fname)
        return []
    total_frames = frame_count
    sampling_period = max((total_frames // n_clips), 1)
    n_snipets = min(n_clips, (total_frames // sampling_period))
    if (not is_validation):
        starts = np.random.randint(0, max(1, (sampling_period - clip_len)), n_snipets)
    else:
        starts = np.zeros(n_snipets)
    offsets = np.arange(0, total_frames, sampling_period)
    selection = np.concatenate([np.arange((of + s), ((of + s) + clip_len)) for (of, s) in zip(offsets, starts)])
    frames = []
    count = ret_count = 0
    while (count < (selection[(- 1)] + clip_len)):
        (retained, frame) = capture.read()
        if (count not in selection):
            count += 1
            continue
        if (not retained):
            if (len(frames) > 0):
                frame = np.copy(frames[(- 1)])
            else:
                frame = (255 * np.random.rand(frame_height, frame_width, 3)).astype('uint8')
            frames.append(frame)
            ret_count += 1
            count += 1
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
        count += 1
    capture.release()
    frames = np.stack(frames)
    total = (n_clips * clip_len)
    while (frames.shape[0] < total):
        frames = np.concatenate([frames, frames[:(total - frames.shape[0])]])
    frames = frames.reshape([n_clips, clip_len, frame_height, frame_width, 3])
    return frames

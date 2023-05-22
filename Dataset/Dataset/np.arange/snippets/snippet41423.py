import os, numpy as np
import simplejson as json
import cv2
from tqdm import tqdm
from skimage.transform import resize
from joblib import Parallel, delayed
import multiprocessing


def load_clips_npy(fname, clip_len=16, n_clips=1, is_validation=False):
    if (not os.path.exists(fname)):
        return []
    try:
        clip = np.load(fname, mmap_mode='r')
    except ValueError:
        print('MMAP ERROR!!')
        return []
    (frame_count, H, W, ch) = clip.shape
    total_frames = min(frame_count, 300)
    sampling_period = max((total_frames // n_clips), 1)
    n_snipets = min(n_clips, (total_frames // sampling_period))
    if (not is_validation):
        starts = np.random.randint(0, max(1, (sampling_period - clip_len)), n_snipets)
    else:
        starts = np.zeros(n_snipets)
    offsets = np.arange(0, total_frames, sampling_period)
    selection = np.concatenate([np.arange((of + s), ((of + s) + clip_len)) for (of, s) in zip(offsets, starts)])
    selection = selection[(selection < frame_count)]
    clip = clip[selection.astype(int)]
    total = (n_clips * clip_len)
    while (clip.shape[0] < total):
        clip = np.concatenate([clip, clip[:(total - clip.shape[0])]])
    clip = clip.reshape([n_clips, clip_len, H, W, 3])
    return clip

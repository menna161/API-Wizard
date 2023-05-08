import os
import cv2
import numpy as np
import tqdm
import glob
import zipfile
import urllib.request
from shutil import copyfile


def preprocess_labels(files, out_dir, binary=True):
    commonpath = os.path.commonpath(files)
    for f in tqdm.tqdm(files):
        out = os.path.join(out_dir, os.path.relpath(f, commonpath))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        src = cv2.imread(f)
        src = src[(:, :, 0)]
        dst = np.zeros(src.shape, src.dtype)
        if binary:
            dst[(src != 0)] = 1
        else:
            dst[(src == 70)] = 1
            dst[(src == 160)] = 2
        cv2.imwrite(out, dst)

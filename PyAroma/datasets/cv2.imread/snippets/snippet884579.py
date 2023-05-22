import glob
import math
import os
import random
import shutil
import time
from pathlib import Path
from threading import Thread
import cv2
import numpy as np
import torch
from PIL import Image, ExifTags
from torch.utils.data import Dataset
from tqdm import tqdm
from utils.utils import xyxy2xywh, xywh2xyxy
from skimage import io


def reduce_img_size(path='../data/sm4/images', img_size=1024):
    path_new = (path + '_reduced')
    create_folder(path_new)
    for f in tqdm(glob.glob(('%s/*.*' % path))):
        try:
            img = cv2.imread(f)
            (h, w) = img.shape[:2]
            r = (img_size / max(h, w))
            if (r < 1.0):
                img = cv2.resize(img, (int((w * r)), int((h * r))), interpolation=cv2.INTER_AREA)
            fnew = f.replace(path, path_new)
            cv2.imwrite(fnew, img)
        except:
            print(('WARNING: image failure %s' % f))

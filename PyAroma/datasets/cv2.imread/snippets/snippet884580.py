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


def convert_images2bmp():
    formats = ([x.lower() for x in img_formats] + [x.upper() for x in img_formats])
    for path in ['../data/sm4/images', '../data/sm4/background']:
        create_folder((path + 'bmp'))
        for ext in formats:
            for f in tqdm(glob.glob(('%s/*%s' % (path, ext))), desc=('Converting %s' % ext)):
                cv2.imwrite(f.replace(ext.lower(), '.bmp').replace(path, (path + 'bmp')), cv2.imread(f))
    for file in ['../data/sm4/out_train.txt', '../data/sm4/out_test.txt']:
        with open(file, 'r') as f:
            lines = f.read()
            lines = lines.replace('/images', '/imagesbmp')
            lines = lines.replace('/background', '/backgroundbmp')
        for ext in formats:
            lines = lines.replace(ext, '.bmp')
        with open(file.replace('.txt', 'bmp.txt'), 'w') as f:
            f.write(lines)

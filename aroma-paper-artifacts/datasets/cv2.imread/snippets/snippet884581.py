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


def recursive_dataset2bmp(dataset='../data/sm4_bmp'):
    formats = ([x.lower() for x in img_formats] + [x.upper() for x in img_formats])
    for (a, b, files) in os.walk(dataset):
        for file in tqdm(files, desc=a):
            p = ((a + '/') + file)
            s = Path(file).suffix
            if (s == '.txt'):
                with open(p, 'r') as f:
                    lines = f.read()
                for f in formats:
                    lines = lines.replace(f, '.bmp')
                with open(p, 'w') as f:
                    f.write(lines)
            elif (s in formats):
                cv2.imwrite(p.replace(s, '.bmp'), cv2.imread(p))
                if (s != '.bmp'):
                    os.system(("rm '%s'" % p))

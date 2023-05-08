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


def load_image(self, index):
    img = self.imgs[index]
    if (img is None):
        img_path = self.img_files[index]
        img = cv2.imread(img_path)
        assert (img is not None), ('Image Not Found ' + img_path)
        (h0, w0) = img.shape[:2]
        r = (self.img_size / max(h0, w0))
        if ((r < 1) or (self.augment and (r != 1))):
            interp = (cv2.INTER_LINEAR if self.augment else cv2.INTER_AREA)
            img = cv2.resize(img, (int((w0 * r)), int((h0 * r))), interpolation=interp)
        return (img, (h0, w0), img.shape[:2])
    else:
        return (self.imgs[index], self.img_hw0[index], self.img_hw[index])

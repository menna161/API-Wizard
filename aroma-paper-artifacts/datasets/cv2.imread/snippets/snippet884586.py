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


def __next__(self):
    if (self.count == self.nF):
        raise StopIteration
    path = self.files[self.count]
    if self.video_flag[self.count]:
        self.mode = 'video'
        (ret_val, img0) = self.cap.read()
        if (not ret_val):
            self.count += 1
            self.cap.release()
            if (self.count == self.nF):
                raise StopIteration
            else:
                path = self.files[self.count]
                self.new_video(path)
                (ret_val, img0) = self.cap.read()
        self.frame += 1
        print(('video %g/%g (%g/%g) %s: ' % ((self.count + 1), self.nF, self.frame, self.nframes, path)), end='')
    else:
        self.count += 1
        img0 = cv2.imread(path)
        assert (img0 is not None), ('Image Not Found ' + path)
        print(('image %g/%g %s: ' % (self.count, self.nF, path)), end='')
    img = letterbox(img=img0, new_shape=self.img_size, auto=self.auto)[0]
    img = img[(:, :, ::(- 1))].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    return (path, img, img0, self.cap)

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


def load_mosaic(self, index):
    labels4 = []
    s = self.img_size
    (xc, yc) = [int(random.uniform((s * 0.5), (s * 1.5))) for _ in range(2)]
    img4 = (np.zeros(((s * 2), (s * 2), 3), dtype=np.uint8) + 128)
    indices = ([index] + [random.randint(0, (len(self.labels) - 1)) for _ in range(3)])
    for (i, index) in enumerate(indices):
        (img, _, (h, w)) = load_image(self, index)
        if (i == 0):
            (x1a, y1a, x2a, y2a) = (max((xc - w), 0), max((yc - h), 0), xc, yc)
            (x1b, y1b, x2b, y2b) = ((w - (x2a - x1a)), (h - (y2a - y1a)), w, h)
        elif (i == 1):
            (x1a, y1a, x2a, y2a) = (xc, max((yc - h), 0), min((xc + w), (s * 2)), yc)
            (x1b, y1b, x2b, y2b) = (0, (h - (y2a - y1a)), min(w, (x2a - x1a)), h)
        elif (i == 2):
            (x1a, y1a, x2a, y2a) = (max((xc - w), 0), yc, xc, min((s * 2), (yc + h)))
            (x1b, y1b, x2b, y2b) = ((w - (x2a - x1a)), 0, max(xc, w), min((y2a - y1a), h))
        elif (i == 3):
            (x1a, y1a, x2a, y2a) = (xc, yc, min((xc + w), (s * 2)), min((s * 2), (yc + h)))
            (x1b, y1b, x2b, y2b) = (0, 0, min(w, (x2a - x1a)), min((y2a - y1a), h))
        img4[(y1a:y2a, x1a:x2a)] = img[(y1b:y2b, x1b:x2b)]
        padw = (x1a - x1b)
        padh = (y1a - y1b)
        label_path = self.label_files[index]
        if os.path.isfile(label_path):
            x = self.labels[index]
            if (x is None):
                with open(label_path, 'r') as f:
                    x = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)
            if (x.size > 0):
                labels = x.copy()
                labels[(:, 1)] = ((w * (x[(:, 1)] - (x[(:, 3)] / 2))) + padw)
                labels[(:, 2)] = ((h * (x[(:, 2)] - (x[(:, 4)] / 2))) + padh)
                labels[(:, 3)] = ((w * (x[(:, 1)] + (x[(:, 3)] / 2))) + padw)
                labels[(:, 4)] = ((h * (x[(:, 2)] + (x[(:, 4)] / 2))) + padh)
            else:
                labels = np.zeros((0, 5), dtype=np.float32)
            labels4.append(labels)
    if len(labels4):
        labels4 = np.concatenate(labels4, 0)
        np.clip(labels4[(:, 1:)], 0, (2 * s), out=labels4[(:, 1:)])
    (img4, labels4) = random_affine(img4, labels4, degrees=(self.hyp['degrees'] * 1), translate=(self.hyp['translate'] * 1), scale=(self.hyp['scale'] * 1), shear=(self.hyp['shear'] * 1), border=((- s) // 2))
    return (img4, labels4)

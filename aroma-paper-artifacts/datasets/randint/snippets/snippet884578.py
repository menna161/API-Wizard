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


def cutout(image, labels):
    (h, w) = image.shape[:2]

    def bbox_ioa(box1, box2):
        box2 = box2.transpose()
        (b1_x1, b1_y1, b1_x2, b1_y2) = (box1[0], box1[1], box1[2], box1[3])
        (b2_x1, b2_y1, b2_x2, b2_y2) = (box2[0], box2[1], box2[2], box2[3])
        inter_area = ((np.minimum(b1_x2, b2_x2) - np.maximum(b1_x1, b2_x1)).clip(0) * (np.minimum(b1_y2, b2_y2) - np.maximum(b1_y1, b2_y1)).clip(0))
        box2_area = (((b2_x2 - b2_x1) * (b2_y2 - b2_y1)) + 1e-16)
        return (inter_area / box2_area)
    scales = ((((([0.5] * 1) + ([0.25] * 2)) + ([0.125] * 4)) + ([0.0625] * 8)) + ([0.03125] * 16))
    for s in scales:
        mask_h = random.randint(1, int((h * s)))
        mask_w = random.randint(1, int((w * s)))
        xmin = max(0, (random.randint(0, w) - (mask_w // 2)))
        ymin = max(0, (random.randint(0, h) - (mask_h // 2)))
        xmax = min(w, (xmin + mask_w))
        ymax = min(h, (ymin + mask_h))
        image[(ymin:ymax, xmin:xmax)] = [random.randint(64, 191) for _ in range(3)]
        if (len(labels) and (s > 0.03)):
            box = np.array([xmin, ymin, xmax, ymax], dtype=np.float32)
            ioa = bbox_ioa(box, labels[(:, 1:5)])
            labels = labels[(ioa < 0.6)]
    return labels

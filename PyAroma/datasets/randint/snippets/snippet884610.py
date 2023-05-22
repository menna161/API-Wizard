from __future__ import division
import math
import time
import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import random
from torch2trt import torch2trt
import torchvision


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    tl = (line_thickness or (round(((0.002 * (img.shape[0] + img.shape[1])) / 2)) + 1))
    color = (color or [random.randint(0, 255) for _ in range(3)])
    (c1, c2) = ((int(x[0]), int(x[1])), (int(x[2]), int(x[3])))
    cv2.rectangle(img, c1, c2, color, thickness=tl)
    if label:
        tf = max((tl - 1), 1)
        t_size = cv2.getTextSize(label, 0, fontScale=(tl / 3), thickness=tf)[0]
        c2 = ((c1[0] + t_size[0]), ((c1[1] - t_size[1]) - 3))
        cv2.rectangle(img, c1, c2, color, (- 1))
        cv2.putText(img, label, (c1[0], (c1[1] - 2)), 0, (tl / 3), [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

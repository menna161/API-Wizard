from __future__ import division
from models_rect import *
from utils.utils import *
from utils.datasets import *
import os
import sys
import time
import datetime
import argparse
from PIL import Image
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator
from torch2trt import TRTModule
from torchstat import stat
from torch2trt import torch2trt
from pathlib import Path


def Vedio_show(pred, last_img0, names):
    '\n    画图+显示视频用\n    '
    colors = [[0, 0, 255], [0, 255, 0]]
    for (i, det) in enumerate(pred):
        (p, s, im0) = (path, '', last_img0)
        if ((det is not None) and len(det)):
            det[(:, :4)] = scale_coords(img.shape[1:], det[(:, :4)], im0.shape).round()
            for (*xyxy, conf, cls) in det:
                label = ('%s %.2f' % (names[int(cls)], conf))
                plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
    label = (('%.2f' % (1 / (time.time() - t0))) + ' FPS')
    cv2.putText(im0, label, (10, 30), 0, 1, [0, 0, 0], thickness=3, lineType=cv2.LINE_AA)
    cv2.imshow(p, im0)
    if (cv2.waitKey(1) == ord('q')):
        raise StopIteration

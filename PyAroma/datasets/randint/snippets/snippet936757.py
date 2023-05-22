import pickle
import os
import numpy as np
import torch
import warnings
from tqdm import tqdm
from network.tubetk import TubeTK
from apex import amp
import argparse
import multiprocessing
from configs.default import __C, cfg_from_file
from post_processing.tube_iou_matching import matching
import shutil
from Visualization.Vis_Res import vis_one_video
import cv2
import torch.utils.data as data
import random
from dataset.augmentation import SSJAugmentation


def __getitem__(self, item):
    item = (item % len(self.parser))
    (image, img_meta, tubes, labels, start_frame) = self.parser[item]
    while (image is None):
        (image, img_meta, tubes, labels, start_frame) = self.parser[((item + random.randint((- 10), 10)) % len(self.parser))]
        print('None processing.')
    if (self.transform is None):
        return (image, img_meta, tubes, labels, start_frame)
    else:
        (image, img_meta, tubes, labels, start_frame) = self.transform(image, img_meta, tubes, labels, start_frame)
        return (image, img_meta, tubes, labels, start_frame)

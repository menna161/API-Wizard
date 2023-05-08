from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
import cv2
import bisect
import random
import torch.distributed as dist


def cv2_loader(img_str):
    return cv2.imread(img_str, cv2.IMREAD_COLOR)

import os.path as osp
import cv2
import jpeg4py as jpeg
import torch
from torch.utils.data import Dataset
from torchvision.datasets import DatasetFolder


def cv2_loader(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

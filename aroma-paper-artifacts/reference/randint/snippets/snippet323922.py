import os
import numpy as np
import torch
import torch.nn as nn
import cv2
import random
import PIL
from PIL import Image
from torch.utils.data import Sampler
import torchvision.transforms as transforms
import math
import torchvision.datasets as datasets


def __iter__(self):
    random.seed(self.rank)
    for i in range(self.total_iters):
        batch_iter = []
        for _ in range(self.batch_size):
            batch_iter.append(random.randint(0, (self.dataset_num - 1)))
        (yield batch_iter)

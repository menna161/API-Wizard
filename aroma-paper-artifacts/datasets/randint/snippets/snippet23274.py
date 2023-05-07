from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_url, check_integrity
from base.torchvision_dataset import TorchvisionDataset
from PIL.ImageFilter import GaussianBlur
import numpy as np
import torch
import torchvision.transforms as transforms
import random
import os


def __getitem__(self, index):
    '\n        Args:\n            index (int): Index\n\n        Returns:\n            tuple: (image, target, semi_target, index)\n        '
    index = ((index + self.offset) % self.size)
    index = self.idxs[index]
    if self.exclude_cifar:
        while self.in_cifar(index):
            index = np.random.randint(79302016)
    img = self.load_image(index)
    if (self.transform is not None):
        img = self.transform(img)
    return (img, 1, (- 1), index)

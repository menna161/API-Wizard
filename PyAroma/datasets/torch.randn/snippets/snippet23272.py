from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_url, check_integrity
from base.torchvision_dataset import TorchvisionDataset
from PIL.ImageFilter import GaussianBlur
import numpy as np
import torch
import torchvision.transforms as transforms
import random
import os


def __init__(self, root: str, data_augmentation: bool=True, normalize: bool=False, size: int=79302016, blur_oe: bool=False, blur_std: float=1.0, seed: int=0):
    super().__init__(root)
    self.image_size = (3, 32, 32)
    self.n_classes = 1
    self.shuffle = False
    self.size = size
    transform = [transforms.ToTensor(), transforms.ToPILImage()]
    if data_augmentation:
        transform += [transforms.ColorJitter(brightness=0.01, contrast=0.01, saturation=0.01, hue=0.01), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomCrop(32, padding=4)]
    else:
        transform += [transforms.CenterCrop(32)]
    if blur_oe:
        transform += [transforms.Lambda((lambda x: x.filter(GaussianBlur(radius=blur_std))))]
    transform += [transforms.ToTensor()]
    if data_augmentation:
        transform += [transforms.Lambda((lambda x: (x + (0.001 * torch.randn_like(x)))))]
    if normalize:
        transform += [transforms.Normalize((0.491373, 0.482353, 0.446667), (0.247059, 0.243529, 0.261569))]
    transform = transforms.Compose(transform)
    self.train_set = TinyImages(root=self.root, size=self.size, transform=transform, download=True, seed=seed)
    self.test_set = None

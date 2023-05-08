from torch.utils.data import Subset
from PIL import Image
from torchvision.datasets import CIFAR100
from base.torchvision_dataset import TorchvisionDataset
import numpy as np
import torch
import torchvision.transforms as transforms
import random


def __init__(self, root: str, normal_class: int=0, data_augmentation: bool=False, normalize: bool=False, outlier_exposure: bool=False, oe_n_classes: int=100, seed: int=0):
    super().__init__(root)
    self.image_size = (3, 32, 32)
    self.n_classes = 2
    self.shuffle = True
    random.seed(seed)
    if outlier_exposure:
        self.normal_classes = None
        self.outlier_classes = list(range(0, 100))
        self.known_outlier_classes = tuple(random.sample(self.outlier_classes, oe_n_classes))
    else:
        self.normal_classes = tuple([normal_class])
        self.outlier_classes = list(range(0, 100))
        self.outlier_classes.remove(normal_class)
        self.outlier_classes = tuple(self.outlier_classes)
    train_transform = []
    test_transform = []
    if data_augmentation:
        train_transform += [transforms.ColorJitter(brightness=0.01, contrast=0.01, saturation=0.01, hue=0.01), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomCrop(32, padding=4)]
    train_transform += [transforms.ToTensor()]
    test_transform += [transforms.ToTensor()]
    if data_augmentation:
        train_transform += [transforms.Lambda((lambda x: (x + (0.001 * torch.randn_like(x)))))]
    if normalize:
        train_transform += [transforms.Normalize((0.491373, 0.482353, 0.446667), (0.247059, 0.243529, 0.261569))]
        test_transform += [transforms.Normalize((0.491373, 0.482353, 0.446667), (0.247059, 0.243529, 0.261569))]
    train_transform = transforms.Compose(train_transform)
    test_transform = transforms.Compose(test_transform)
    target_transform = transforms.Lambda((lambda x: int((x in self.outlier_classes))))
    train_set = MyCIFAR100(root=self.root, train=True, transform=train_transform, target_transform=target_transform, download=True)
    if outlier_exposure:
        idx = np.argwhere(np.isin(np.array(train_set.targets), self.known_outlier_classes))
        idx = idx.flatten().tolist()
        train_set.semi_targets[idx] = ((- 1) * torch.ones(len(idx)).long())
        self.train_set = Subset(train_set, idx)
        self.train_set.shuffle_idxs = False
        self.test_set = None
    else:
        idx = np.argwhere(np.isin(np.array(train_set.targets), self.normal_classes))
        idx = idx.flatten().tolist()
        train_set.semi_targets[idx] = torch.zeros(len(idx)).long()
        self.train_set = Subset(train_set, idx)
        self.test_set = MyCIFAR100(root=self.root, train=False, transform=test_transform, target_transform=target_transform, download=True)

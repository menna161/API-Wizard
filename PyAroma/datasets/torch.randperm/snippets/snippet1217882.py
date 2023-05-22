import torch
import torchvision.transforms as transforms
import random


def __call__(self, img):
    if (self.transforms is None):
        return img
    order = torch.randperm(len(self.transforms))
    for i in order:
        img = self.transforms[i](img)
    return img

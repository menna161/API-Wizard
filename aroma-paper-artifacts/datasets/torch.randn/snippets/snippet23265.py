from torchvision.datasets import ImageFolder
from base.torchvision_dataset import TorchvisionDataset
from PIL.ImageFilter import GaussianBlur
import torch
import torchvision.transforms as transforms
import random


def __init__(self, root: str, data_augmentation: bool=True, normalize: bool=False, size: int=14155519, blur_oe: bool=False, blur_std: float=1.0, seed: int=0):
    super().__init__(root)
    self.image_size = (3, 224, 224)
    self.n_classes = 1
    self.shuffle = False
    self.size = size
    transform = [transforms.Resize(256)]
    if data_augmentation:
        transform += [transforms.ColorJitter(brightness=0.01, contrast=0.01, saturation=0.01, hue=0.01), transforms.RandomHorizontalFlip(p=0.5), transforms.RandomCrop(224)]
    else:
        transform += [transforms.CenterCrop(224)]
    if blur_oe:
        transform += [transforms.Lambda((lambda x: x.filter(GaussianBlur(radius=blur_std))))]
    transform += [transforms.ToTensor()]
    if data_augmentation:
        transform += [transforms.Lambda((lambda x: (x + (0.001 * torch.randn_like(x)))))]
    if normalize:
        transform += [transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))]
    transform = transforms.Compose(transform)
    self.train_set = MyImageNet22K(root=(self.root + '/fall11_whole_extracted'), size=self.size, transform=transform, seed=seed)
    self.test_set = None

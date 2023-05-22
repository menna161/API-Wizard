import os
import sys
import numpy as np
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torch
from .transforms import *
from .dataloader import MyDataloader
from transforms import *
from dataloader import MyDataloader

if (__name__ == '__main__'):
    HOME = os.environ['HOME']
    rgbdir = (HOME + '/myDataset/NYU_v2/')
    depdir = (HOME + '/myDataset/NYU_v2/')
    trainrgb = '../datasets/nyu_path/train_rgb_12k.txt'
    traindep = '../datasets/nyu_path/train_depth_12k.txt'
    valrgb = '../datasets/nyu_path/valid_rgb.txt'
    valdep = '../datasets/nyu_path/valid_depth.txt'
    kwargs = {'min_depth': 0.72, 'max_depth': 10.0, 'flip': True, 'scale': True, 'rotate': True, 'jitter': True, 'crop': True}
    train_dataset = NYUDataset(rgbdir, depdir, trainrgb, traindep, mode='train', **kwargs)
    val_dataset = NYUDataset(rgbdir, depdir, valrgb, valdep, mode='val', **kwargs)
    trainloader = DataLoader(train_dataset, 20, shuffle=True, num_workers=4, pin_memory=True, drop_last=False)
    valloader = DataLoader(val_dataset, 20, shuffle=True, num_workers=4, pin_memory=True, drop_last=False)
    (image, label) = train_dataset[2000]
    image_npy = image.numpy().transpose(1, 2, 0)
    label_npy = label.numpy().squeeze()
    print(image.shape, label.shape)
    print(label.max())
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(image_npy)
    plt.subplot(1, 2, 2)
    plt.imshow(label_npy, cmap='jet')
    plt.show()

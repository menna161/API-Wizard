import os
import sys
import numpy as np
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from .transforms import *
from .dataloader import MyDataloader
from transforms import *
from dataloader import MyDataloader

if (__name__ == '__main__'):
    HOME = os.environ['HOME']
    rgbdir = (HOME + '/myDataset/KITTI/raw_data_KITTI/')
    depdir = (HOME + '/myDataset/KITTI/datasets_KITTI/')
    trainrgb = '../datasets/kitti_path/eigen_train_files.txt'
    traindep = '../datasets/kitti_path/eigen_train_depth_files.txt'
    valrgb = '../datasets/kitti_path/eigen_test_files.txt'
    valdep = '../datasets/kitti_path/eigen_test_depth_files.txt'
    kwargs = {'min_depth': 1.8, 'max_depth': 80.0, 'flip': True, 'scale': True, 'rotate': True, 'jitter': True, 'crop': True}
    train_dataset = KITTIDataset(rgbdir, depdir, trainrgb, traindep, mode='train', **kwargs)
    val_dataset = KITTIDataset(rgbdir, depdir, valrgb, valdep, mode='val', **kwargs)
    trainloader = DataLoader(train_dataset, 10, shuffle=True, num_workers=4, pin_memory=True, drop_last=False)
    valloader = DataLoader(val_dataset, 10, shuffle=True, num_workers=4, pin_memory=True, drop_last=False)
    (image, label) = train_dataset[400]
    image_npy = image.numpy().transpose(1, 2, 0)
    label_npy = label.numpy().squeeze()
    print(image.shape, label.shape)
    print(label.max())
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(image_npy)
    plt.subplot(1, 2, 2)
    plt.imshow(label_npy, cmap='plasma')
    plt.show()

import torch.optim
from torchvision import datasets, transforms
import torch.nn.functional as F
from kymatio import Scattering2D
import torch
import argparse
import kymatio.datasets as scattering_datasets
import torch.nn as nn
from numpy.random import RandomState
import numpy as np


def main():
    'Train a simple Hybrid Resnet Scattering + CNN model on CIFAR.\n\n    '
    parser = argparse.ArgumentParser(description='CIFAR scattering  + hybrid examples')
    parser.add_argument('--mode', type=str, default='scattering', choices=['scattering', 'standard'], help='network_type')
    parser.add_argument('--num_samples', type=int, default=50, help='samples per class')
    parser.add_argument('--learning_schedule_multi', type=int, default=10, help='samples per class')
    parser.add_argument('--seed', type=int, default=0, help='seed for dataset subselection')
    parser.add_argument('--width', type=int, default=2, help='width factor for resnet')
    args = parser.parse_args()
    use_cuda = torch.cuda.is_available()
    device = torch.device(('cuda' if use_cuda else 'cpu'))
    if (args.mode == 'scattering'):
        scattering = Scattering2D(J=2, shape=(32, 32))
        K = (81 * 3)
        model = Scattering2dResNet(K, args.width).to(device)
        scattering = scattering.to(device)
    else:
        model = Scattering2dResNet(8, args.width, standard=True).to(device)
        scattering = Identity()
    num_workers = 4
    if use_cuda:
        pin_memory = True
    else:
        pin_memory = False
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    cifar_data = datasets.CIFAR10(root=scattering_datasets.get_dataset_dir('CIFAR'), train=True, transform=transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomCrop(32, 4), transforms.ToTensor(), normalize]), download=True)
    prng = RandomState(args.seed)
    random_permute = prng.permutation(np.arange(0, 5000))[0:args.num_samples]
    indx = np.concatenate([np.where((np.array(cifar_data.targets) == classe))[0][random_permute] for classe in range(0, 10)])
    (cifar_data.data, cifar_data.targets) = (cifar_data.data[indx], list(np.array(cifar_data.targets)[indx]))
    train_loader = torch.utils.data.DataLoader(cifar_data, batch_size=32, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    test_loader = torch.utils.data.DataLoader(datasets.CIFAR10(root=scattering_datasets.get_dataset_dir('CIFAR'), train=False, transform=transforms.Compose([transforms.ToTensor(), normalize])), batch_size=128, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)
    lr = 0.1
    M = args.learning_schedule_multi
    drops = [(60 * M), (120 * M), (160 * M)]
    for epoch in range(0, (200 * M)):
        if ((epoch in drops) or (epoch == 0)):
            optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)
            lr *= 0.2
        train(model, device, train_loader, optimizer, (epoch + 1), scattering)
        if ((epoch % 10) == 0):
            test(model, device, test_loader, scattering)

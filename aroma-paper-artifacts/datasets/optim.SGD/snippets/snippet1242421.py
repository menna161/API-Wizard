import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim
from torchvision import datasets, transforms
from kymatio.torch import Scattering2D
import kymatio.datasets as scattering_datasets
import argparse

if (__name__ == '__main__'):
    'Train a simple Hybrid Resnet Scattering + CNN model on CIFAR.\n\n        scattering 1st order can also be set by the mode\n        Scattering features are normalized by batch normalization.\n        The model achieves around 88% testing accuracy after 10 epochs.\n\n        scatter 1st order +\n        scatter 2nd order + linear achieves 70.5% in 90 epochs\n\n        scatter + cnn achieves 88% in 15 epochs\n\n    '
    parser = argparse.ArgumentParser(description='CIFAR scattering  + hybrid examples')
    parser.add_argument('--mode', type=int, default=1, help='scattering 1st or 2nd order')
    parser.add_argument('--width', type=int, default=2, help='width factor for resnet')
    args = parser.parse_args()
    use_cuda = torch.cuda.is_available()
    device = torch.device(('cuda' if use_cuda else 'cpu'))
    if (args.mode == 1):
        scattering = Scattering2D(J=2, shape=(32, 32), max_order=1)
        K = (17 * 3)
    else:
        scattering = Scattering2D(J=2, shape=(32, 32))
        K = (81 * 3)
    scattering = scattering.to(device)
    model = Scattering2dResNet(K, args.width).to(device)
    num_workers = 4
    if use_cuda:
        pin_memory = True
    else:
        pin_memory = False
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    train_loader = torch.utils.data.DataLoader(datasets.CIFAR10(root=scattering_datasets.get_dataset_dir('CIFAR'), train=True, transform=transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomCrop(32, 4), transforms.ToTensor(), normalize]), download=True), batch_size=128, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    test_loader = torch.utils.data.DataLoader(datasets.CIFAR10(root=scattering_datasets.get_dataset_dir('CIFAR'), train=False, transform=transforms.Compose([transforms.ToTensor(), normalize])), batch_size=128, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)
    lr = 0.1
    for epoch in range(0, 90):
        if ((epoch % 20) == 0):
            optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)
            lr *= 0.2
        train(model, device, train_loader, optimizer, (epoch + 1), scattering)
        test(model, device, test_loader, scattering)

import os, math
import numpy as np
import time
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from lib.utils.meter import Meter
from model import SSNModel
from lib.dataset import bsds, augmentation
from lib.utils.loss import reconstruct_loss_with_cross_etnropy, reconstruct_loss_with_mse
import argparse


def train(cfg):
    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'
    model = SSNModel(cfg.fdim, cfg.nspix, cfg.niter).to(device)
    optimizer = optim.Adam(model.parameters(), cfg.lr)
    augment = augmentation.Compose([augmentation.RandomHorizontalFlip(), augmentation.RandomScale(), augmentation.RandomCrop()])
    train_dataset = bsds.BSDS(cfg.root, geo_transforms=augment)
    train_loader = DataLoader(train_dataset, cfg.batchsize, shuffle=True, drop_last=True, num_workers=cfg.nworkers)
    test_dataset = bsds.BSDS(cfg.root, split='val')
    test_loader = DataLoader(test_dataset, 1, shuffle=False, drop_last=False)
    meter = Meter()
    iterations = 0
    max_val_asa = 0
    while (iterations < cfg.train_iter):
        for data in train_loader:
            iterations += 1
            metric = update_param(data, model, optimizer, cfg.compactness, cfg.color_scale, cfg.pos_scale, device)
            meter.add(metric)
            state = meter.state(f'[{iterations}/{cfg.train_iter}]')
            print(state)
            if ((iterations % cfg.test_interval) == 0):
                asa = eval(model, test_loader, cfg.color_scale, cfg.pos_scale, device)
                print(f'validation asa {asa}')
                if (asa > max_val_asa):
                    max_val_asa = asa
                    torch.save(model.state_dict(), os.path.join(cfg.out_dir, 'bset_model.pth'))
            if (iterations == cfg.train_iter):
                break
    unique_id = str(int(time.time()))
    torch.save(model.state_dict(), os.path.join(cfg.out_dir, (('model' + unique_id) + '.pth')))

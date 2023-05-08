import argparse
import json
import math
import os
import random
import time
from os import path
import numpy as np
import torch
import torch.nn.init as init
import torch.optim as optim
from datasets import CartPoleDataset, PendulumDataset, PlanarDataset, ThreePoleDataset
from losses import curvature, nce_past
from pc3_model import PC3
from tensorboardX import SummaryWriter
from torch import nn
from torch.utils.data import DataLoader


def train(model, option, train_loader, lam, latent_noise, optimizer, armotized, epoch):
    avg_nce_loss = 0.0
    avg_consis_loss = 0.0
    avg_cur_loss = 0.0
    avg_norm_loss = 0.0
    avg_norm_2_loss = 0.0
    avg_loss = 0.0
    num_batches = len(train_loader)
    model.train()
    start = time.time()
    for (iter, (x, u, x_next)) in enumerate(train_loader):
        x = x.to(device).double()
        u = u.to(device).double()
        x_next = x_next.to(device).double()
        optimizer.zero_grad()
        (z_enc, z_next_trans_dist, z_next_enc) = model(x, u, x_next)
        noise = (torch.randn(size=z_next_enc.size()) * latent_noise)
        if next(model.encoder.parameters()).is_cuda:
            noise = noise.cuda()
        z_next_enc += noise
        (nce_loss, consis_loss, cur_loss, norm_loss, norm_2, loss) = compute_loss(model, armotized, u, z_enc, z_next_trans_dist, z_next_enc, option, lam=lam)
        loss.backward()
        optimizer.step()
        avg_nce_loss += nce_loss.item()
        avg_consis_loss += consis_loss.item()
        avg_cur_loss += cur_loss.item()
        avg_norm_loss += norm_loss.item()
        avg_norm_2_loss += norm_2.item()
        avg_loss += loss.item()
    avg_nce_loss /= num_batches
    avg_consis_loss /= num_batches
    avg_cur_loss /= num_batches
    avg_norm_loss /= num_batches
    avg_norm_2_loss /= num_batches
    avg_loss /= num_batches
    if (((epoch + 1) % 1) == 0):
        print(('Epoch %d' % (epoch + 1)))
        print(('NCE loss: %f' % avg_nce_loss))
        print(('Consistency loss: %f' % avg_consis_loss))
        print(('Curvature loss: %f' % avg_cur_loss))
        print(('Normalization loss: %f' % avg_norm_loss))
        print(('Norma 2 loss: %f' % avg_norm_2_loss))
        print(('Training loss: %f' % avg_loss))
        print(('Training time: %f' % (time.time() - start)))
        print('--------------------------------------')
    return (avg_nce_loss, avg_consis_loss, avg_cur_loss, avg_loss)

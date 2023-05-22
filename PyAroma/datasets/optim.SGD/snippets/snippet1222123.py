import os
import random
import time
import cv2
import numpy as np
import logging
import argparse
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.multiprocessing as mp
import torch.distributed as dist
import torch.nn.init as initer
from tensorboardX import SummaryWriter
import sys
from utils import dataset, transform, common
from models import fastscnn
from loss import diceloss


def train():
    device = (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
    model = fastscnn.FastSCNN(numClasses, True)
    numParams = sum((torch.numel(p) for p in model.parameters()))
    print(f'Total paramers: {numParams}')
    model = model.to(device)
    weightsInit(model)
    (mean, std) = getMeanStd()
    criterion = diceloss.DiceLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=baseLr, momentum=0.9, weight_decay=0.0001)
    (trainDataLoader, valDataLoader) = prepareDataset(dataRoot, trainList, valList, mean, std)
    maxIter = (globalEpoch * len(trainDataLoader))
    for epoch in range(1, globalEpoch):
        subTrain(model, optimizer, criterion, trainDataLoader, epoch, maxIter, device)
        subVal(model, criterion, valDataLoader, device)
        if ((epoch % 20) == 0):
            filename = ((('save/' + 'train_') + str(epoch)) + '.pth')
            torch.save({'epoch': epoch, 'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}, filename)

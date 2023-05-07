import argparse
import os
from datetime import datetime
from os.path import join as pjoin
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from tensorboardX import SummaryWriter
from torch.utils import data
from tqdm import tqdm
import core.loss
import torchvision.utils as vutils
from core.augmentations import Compose, RandomHorizontallyFlip, RandomRotate, AddNoise
from core.loader.data_loader import *
from core.metrics import runningScore
from core.models import get_model
from core.utils import np_to_tb


def __iter__(self):
    char = [('i' if (np.random.randint(2) == 1) else 'x')]
    self.indices = [idx for (idx, name) in enumerate(train_list) if (char[0] in name)]
    return (self.indices[i] for i in torch.randperm(len(self.indices)))

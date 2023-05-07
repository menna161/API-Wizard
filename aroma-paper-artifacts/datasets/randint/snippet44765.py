import os
import errno
import numpy as np
from PIL import Image
import torchvision.datasets as dset
import sys
from copy import deepcopy
import argparse
import math
import torch.utils.data as data
import torch
import torch.nn.init
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.backends.cudnn as cudnn
from tqdm import tqdm
import random
import cv2
import copy
from Utils import str2bool
import json
from pprint import pprint


def generate_pairs(self, labels, n_pairs):
    pairs = []
    n_classes = len(labels)
    already_idxs = set()
    for x in tqdm(range(n_pairs)):
        if (len(already_idxs) >= self.batch_size):
            already_idxs = set()
        c1 = np.random.randint(0, n_classes)
        while (c1 in already_idxs):
            c1 = np.random.randint(0, n_classes)
        while (len(labels[c1]) < 3):
            c1 = np.random.randint(0, n_classes)
        already_idxs.add(c1)
        if (len(labels[c1]) == 2):
            (n1, n2) = (0, 1)
        else:
            n1 = np.random.randint(0, len(labels[c1]))
            while (self.patches[(labels[c1][n1], :, :, :)].float().std() < 0.01):
                n1 = np.random.randint(0, len(labels[c1]))
            n2 = np.random.randint(0, len(labels[c1]))
            while (self.patches[(labels[c1][n2], :, :, :)].float().std() < 0.01):
                n2 = np.random.randint(0, len(labels[c1]))
        pairs.append([labels[c1][n1], labels[c1][n2]])
    return torch.LongTensor(np.array(pairs))

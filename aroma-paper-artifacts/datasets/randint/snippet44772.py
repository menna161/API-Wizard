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


def generate_triplets(self, labels, num_triplets, batch_size):

    def create_indices(_labels):
        inds = dict()
        for (idx, ind) in enumerate(_labels):
            if (ind not in inds):
                inds[ind] = []
            inds[ind].append(idx)
        return inds
    triplets = []
    indices = create_indices(labels)
    unique_labels = np.unique(labels.numpy())
    n_classes = unique_labels.shape[0]
    already_idxs = set()
    for x in tqdm(range(num_triplets)):
        if (len(already_idxs) >= batch_size):
            already_idxs = set()
        c1 = np.random.randint(0, n_classes)
        while (c1 in already_idxs):
            c1 = np.random.randint(0, n_classes)
        already_idxs.add(c1)
        c2 = np.random.randint(0, n_classes)
        while (c1 == c2):
            c2 = np.random.randint(0, n_classes)
        if (len(indices[c1]) == 2):
            (n1, n2) = (0, 1)
        else:
            n1 = np.random.randint(0, len(indices[c1]))
            n2 = np.random.randint(0, len(indices[c1]))
            while (n1 == n2):
                n2 = np.random.randint(0, len(indices[c1]))
        n3 = np.random.randint(0, len(indices[c2]))
        triplets.append([indices[c1][n1], indices[c1][n2], indices[c2][n3]])
    return torch.LongTensor(np.array(triplets))

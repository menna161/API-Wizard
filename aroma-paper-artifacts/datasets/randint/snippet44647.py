from __future__ import division, print_function
import sys
from copy import deepcopy
import argparse
import torch
import torch.nn.init
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.backends.cudnn as cudnn
import os
from tqdm import tqdm
import numpy as np
import random
import cv2
import copy
from EvalMetrics import ErrorRateAt95Recall
from Loggers import Logger, FileLogger
from W1BS import w1bs_extract_descs_and_save
from Utils import L2Norm, cv2_scale, np_reshape
from Utils import str2bool
import torch.utils.data as data
import torch.utils.data as data_utils
import torch.nn.functional as F
from Losses import loss_HardNet, loss_random_sampling, loss_L2Net
import faiss
from matplotlib.pyplot import figure, imshow, axis
from pytorch_sift import SIFTNet
import utils.w1bs as w1bs


@staticmethod
def generate_triplets(labels, num_triplets):

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
        if (len(already_idxs) >= args.batch_size):
            already_idxs = set()
        c1 = np.random.randint(0, (n_classes - 1))
        while (c1 in already_idxs):
            c1 = np.random.randint(0, (n_classes - 1))
        already_idxs.add(c1)
        c2 = np.random.randint(0, (n_classes - 1))
        while (c1 == c2):
            c2 = np.random.randint(0, (n_classes - 1))
        if (len(indices[c1]) == 2):
            (n1, n2) = (0, 1)
        else:
            n1 = np.random.randint(0, (len(indices[c1]) - 1))
            n2 = np.random.randint(0, (len(indices[c1]) - 1))
            while (n1 == n2):
                n2 = np.random.randint(0, (len(indices[c1]) - 1))
        n3 = np.random.randint(0, (len(indices[c2]) - 1))
        triplets.append([indices[c1][n1], indices[c1][n2], indices[c2][n3]])
    return torch.LongTensor(np.array(triplets))

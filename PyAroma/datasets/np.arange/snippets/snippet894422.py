import faiss
import os
from os.path import exists, join, basename
from collections import OrderedDict
import numpy as np
import numpy.random
import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.functional import relu
from torch.utils.data import Dataset
from lib.dataloader import DataLoader
from lib.model import ImMatchNet
from lib.im_pair_dataset import ImagePairDataset
from lib.normalization import NormalizeImageDict, normalize_image_dict_caffe
from lib.torch_util import save_checkpoint, str_to_bool
from lib.torch_util import BatchTensorToVars, str_to_bool
from lib.sparse import get_scores
from lib.sparse import corr_and_add
import torch.nn.functional as F
from lib.model import featureL2Norm
import argparse


def weak_loss(model, batch, normalization='softmax', alpha=30):
    if (normalization is None):
        normalize = (lambda x: x)
    elif (normalization == 'softmax'):
        normalize = (lambda x: torch.nn.functional.softmax(x, 1))
    elif (normalization == 'l1'):
        normalize = (lambda x: (x / (torch.sum(x, dim=1, keepdim=True) + 0.0001)))
    b = batch['source_image'].size(0)
    start = torch.cuda.Event(enable_timing=True)
    mid = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    corr4d = model(batch)
    mid.record()
    scores_A = get_scores(corr4d, k=args.k)
    scores_B = get_scores(corr4d, reverse=True, k=args.k)
    score_pos = ((scores_A + scores_B) / 2)
    end.record()
    torch.cuda.synchronize()
    model_time = (start.elapsed_time(mid) / 1000)
    loss_time = (mid.elapsed_time(end) / 1000)
    batch['source_image'] = batch['source_image'][(np.roll(np.arange(b), (- 1)), :)]
    corr4d = model(batch)
    scores_A = get_scores(corr4d, k=args.k)
    scores_B = get_scores(corr4d, reverse=True, k=args.k)
    score_neg = ((scores_A + scores_B) / 2)
    loss = (score_neg - score_pos)
    return loss

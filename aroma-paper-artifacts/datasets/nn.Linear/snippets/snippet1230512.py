import os
import argparse
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision.utils import make_grid
from torch.nn.utils import weight_norm
from utils.misc import add_args
from utils.paths import datasets_path, benchmarks_path
from utils.tensor import to_numpy
from data.base import sample_anchors
from data.multi_emnist import ClusteredMultiEMNIST, sample_idxs, get_train_loader, get_test_loader
from modules.attention import StackedISAB, PMA, MAB
from modules.misc import Flatten, View
from flows.autoregressive import MAF
from flows.distributions import FlowDistribution, Normal, Bernoulli
from models.base import AnchoredFilteringModel, MinFilteringModel


def __init__(self, num_filters=32, dim_lats=128, dim_hids=256, dim_context=256, num_inds=32):
    super().__init__()
    C = num_filters
    self.enc = nn.Sequential(nn.Conv2d(3, C, 3, stride=2), nn.BatchNorm2d(C), nn.ReLU(), nn.Conv2d(C, (2 * C), 3, stride=2), nn.BatchNorm2d((2 * C)), nn.ReLU(), nn.Conv2d((2 * C), (4 * C), 3), Flatten())
    self.isab1 = StackedISAB((((4 * C) * 4) * 4), dim_hids, num_inds, 4)
    self.pma = PMA(dim_hids, dim_hids, 1)
    self.fc1 = nn.Linear(dim_hids, dim_context)
    self.posterior = Normal(dim_lats, use_context=True, context_enc=nn.Linear(((((4 * C) * 4) * 4) + dim_context), (2 * dim_lats)))
    self.prior = FlowDistribution(MAF(dim_lats, dim_hids, 6, dim_context=dim_context, inv_linear=True), Normal(dim_lats))
    self.dec = nn.Sequential(nn.Linear((dim_lats + dim_context), (((4 * C) * 4) * 4)), nn.ReLU(), View((- 1), (4 * C), 4, 4), nn.ConvTranspose2d((4 * C), (2 * C), 3, stride=2, padding=1), nn.BatchNorm2d((2 * C)), nn.ReLU(), nn.ConvTranspose2d((2 * C), C, 3, stride=2, padding=1), nn.BatchNorm2d(C), nn.ReLU(), nn.ConvTranspose2d(C, 3, 3, stride=2, output_padding=1), View((- 1), 3, 28, 28))
    self.likel = Bernoulli((3, 28, 28), use_context=True)
    self.mab = MAB(dim_hids, dim_hids, dim_hids)
    self.isab2 = StackedISAB(dim_hids, dim_hids, num_inds, 4)
    self.fc2 = nn.Linear(dim_hids, 1)

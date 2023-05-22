import argparse
import os
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from data.base import sample_anchors
from utils.paths import benchmarks_path
from utils.misc import add_args
from utils.plots import scatter_mog, draw_ellipse, scatter
from modules.attention import StackedISAB, PMA, MAB
from data.mvn import MultivariateNormalDiag
from data.mog import sample_mog
from models.base import MinFilteringModel, AnchoredFilteringModel


def __init__(self, mvn, dim_hids=128, num_inds=32):
    super().__init__()
    self.mvn = mvn
    self.mab1 = MAB(mvn.dim, mvn.dim, dim_hids)
    self.isab1 = StackedISAB(dim_hids, dim_hids, num_inds, 4)
    self.pma = PMA(dim_hids, dim_hids, 1)
    self.fc1 = nn.Linear(dim_hids, mvn.dim_params)
    self.mab2 = MAB(dim_hids, dim_hids, dim_hids)
    self.isab2 = StackedISAB(dim_hids, dim_hids, num_inds, 4)
    self.fc2 = nn.Linear(dim_hids, 1)

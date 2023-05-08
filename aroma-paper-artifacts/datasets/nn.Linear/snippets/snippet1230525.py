import argparse
import os
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from data.base import sample_anchors
from utils.paths import benchmarks_path
from utils.misc import add_args
from utils.plots import scatter
from utils.tensor import meshgrid_around, to_numpy
from flows.autoregressive import MAF
from flows.distributions import Normal, FlowDistribution
from modules.attention import StackedISAB, PMA, MAB
from data.mog import sample_warped_mog
from models.base import MinFilteringModel, AnchoredFilteringModel


def __init__(self, dim_inputs, dim_hids=128, num_inds=32, dim_context=128, num_blocks=4):
    super().__init__()
    self.flow = FlowDistribution(MAF(dim_inputs, dim_hids, num_blocks, dim_context=dim_context), Normal(dim_inputs, use_context=False))
    self.mab1 = MAB(dim_inputs, dim_inputs, dim_hids)
    self.isab1 = StackedISAB(dim_hids, dim_hids, num_inds, 4)
    self.pma = PMA(dim_hids, dim_hids, 1)
    self.fc1 = nn.Linear(dim_hids, dim_context)
    self.mab2 = MAB(dim_hids, dim_context, dim_hids)
    self.isab2 = StackedISAB(dim_hids, dim_hids, num_inds, 4)
    self.fc2 = nn.Linear(dim_hids, 1)

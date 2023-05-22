import os
import torch
import torch.optim as optim
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from util.visualization import draw_parts_bbox_voxel
from networks import get_network, set_requires_grad
from agent.base import BaseAgent


def set_loss_function(self):
    self.rec_criterion = nn.MSELoss(reduction='none').cuda()
    self.bce_criterion = nn.BCEWithLogitsLoss(reduction='none').cuda()

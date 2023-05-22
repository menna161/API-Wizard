import torch
import torch.nn as nn
from networks import get_network
from agent.base import BaseAgent
from util.visualization import project_voxel_along_xyz, visualize_sdf


def set_loss_function(self):
    self.criterion = nn.MSELoss().cuda()

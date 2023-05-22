import torch.nn as nn
import torch
import torch.nn.functional as F
import util.util as util
from .InnerCosFunction import InnerCosFunction


def __init__(self, crit='MSE', strength=1, skip=0, layer_to_last=3, device='gpu'):
    super(InnerCos, self).__init__()
    self.crit = crit
    self.criterion = (torch.nn.MSELoss() if (self.crit == 'MSE') else torch.nn.L1Loss())
    self.strength = strength
    self.skip = skip
    self.layer_to_last = layer_to_last
    self.device = device
    self.target = torch.tensor(1.0)

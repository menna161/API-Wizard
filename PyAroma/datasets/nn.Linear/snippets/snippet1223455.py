import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def initialize(self):
    for module in self.modules():
        if isinstance(module, (nn.Conv2d, nn.Linear)):
            nn.init.xavier_uniform_(module.weight)
            nn.init.zeros_(module.bias)
    nn.init.xavier_uniform_(self.block2[(- 1)].weight, gain=1e-05)

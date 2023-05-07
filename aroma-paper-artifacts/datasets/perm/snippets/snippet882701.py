import os, sys
import numpy as np
import torch
from utility.utils import device


def apply(self, inputs, target):
    lam = np.random.beta(self.beta, self.beta)
    rand_index = torch.randperm(inputs.size()[0]).to(device)
    target_a = target
    target_b = target[rand_index]
    (bbx1, bby1, bbx2, bby2) = self.rand_bbox(inputs.size(), lam)
    inputs[(:, :, bbx1:bbx2, bby1:bby2)] = inputs[(rand_index, :, bbx1:bbx2, bby1:bby2)]
    lam = (1 - (((bbx2 - bbx1) * (bby2 - bby1)) / (inputs.size()[(- 1)] * inputs.size()[(- 2)])))
    return (target_a, target_b, inputs, lam)

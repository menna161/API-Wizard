import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def forward(self, x_T):
    '\n        Algorithm 2.\n        '
    x_t = x_T
    for time_step in reversed(range(self.T)):
        if ((time_step % 100) == 0):
            print(time_step)
        t = (x_t.new_ones([x_T.shape[0]], dtype=torch.long) * time_step)
        (mean, var) = self.p_mean_variance(x_t=x_t, t=t)
        if (time_step > 0):
            noise = torch.randn_like(x_t)
        else:
            noise = 0
        x_t = (mean + (torch.sqrt(var) * noise))
        assert (torch.isnan(x_t).int().sum() == 0), 'nan in tensor.'
    x_0 = x_t
    return torch.clip(x_0, (- 1), 1)

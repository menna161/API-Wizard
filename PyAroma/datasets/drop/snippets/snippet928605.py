import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def check_if_drop(self):
    current_progress = LearnedGroupConv.global_progress
    delta = 0
    for i in range((self.condense_factor - 1)):
        if ((current_progress * 2) < ((i + 1) / (self.condense_factor - 1))):
            stage = i
            break
    else:
        stage = (self.condense_factor - 1)
    if (not self.reach_stage(stage)):
        self.stage = stage
        delta = (self.in_channels // self.condense_factor)
        print(delta)
    if (delta > 0):
        self.drop(delta)
    return

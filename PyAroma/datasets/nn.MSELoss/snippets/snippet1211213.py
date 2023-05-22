import torch.nn as nn
import torch


def __init__(self):
    super(MSETeacherPointwisePassages, self).__init__()
    self.mse = torch.nn.MSELoss(reduction='none')

import torch.nn as nn
import torch


def __init__(self):
    super(MSETeacherPointwise, self).__init__()
    self.mse = torch.nn.MSELoss()

import torch
import torch.nn as nn


def __init__(self, inp_dim, out_dim, k=3, stride=1):
    super(residual, self).__init__()
    p = ((k - 1) // 2)
    self.conv1 = nn.Conv2d(inp_dim, out_dim, (k, k), padding=(p, p), stride=(stride, stride), bias=False)
    self.bn1 = nn.BatchNorm2d(out_dim)
    self.relu1 = nn.ReLU(inplace=True)
    self.conv2 = nn.Conv2d(out_dim, out_dim, (k, k), padding=(p, p), bias=False)
    self.bn2 = nn.BatchNorm2d(out_dim)
    self.skip = (nn.Sequential(nn.Conv2d(inp_dim, out_dim, (1, 1), stride=(stride, stride), bias=False), nn.BatchNorm2d(out_dim)) if ((stride != 1) or (inp_dim != out_dim)) else nn.Sequential())
    self.relu = nn.ReLU(inplace=True)

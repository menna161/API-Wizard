import matplotlib.pyplot as plt
import numpy as np
import torch
from mpl_toolkits.mplot3d import Axes3D


def init_weights(m):
    if ((type(m) == torch.nn.Conv2d) or (type(m) == torch.nn.ConvTranspose2d) or (type(m) == torch.nn.Conv3d) or (type(m) == torch.nn.ConvTranspose3d)):
        torch.nn.init.kaiming_normal_(m.weight)
        if (m.bias is not None):
            torch.nn.init.constant_(m.bias, 0)
    elif ((type(m) == torch.nn.BatchNorm2d) or (type(m) == torch.nn.BatchNorm3d)):
        torch.nn.init.constant_(m.weight, 1)
        torch.nn.init.constant_(m.bias, 0)
    elif (type(m) == torch.nn.Linear):
        torch.nn.init.normal_(m.weight, 0, 0.01)
        torch.nn.init.constant_(m.bias, 0)

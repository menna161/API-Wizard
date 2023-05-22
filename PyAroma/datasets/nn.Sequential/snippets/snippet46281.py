import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, n_joint1, n_joint2, t_stride, t_kernel, t_padding, drop=0.2, layer1=False, nmp=False):
    super().__init__()
    self.time_conv = nn.Sequential(nn.Conv2d(n_joint1, n_joint1, kernel_size=(t_kernel, 1), stride=(t_stride, 1), padding=(t_padding, 0), bias=True), nn.BatchNorm2d(n_joint1), nn.Dropout(drop, inplace=True))
    if (nmp == True):
        self.mlp1 = Mlp_JpTrans(n_joint2[0], n_joint2[1], n_joint2[1], drop)
        self.mlp2 = Mlp_JpTrans((n_joint2[1] * 2), n_joint2[1], n_joint2[1], drop)
        self.mlp3 = Mlp_JpTrans((n_joint2[1] * 2), n_joint2[1], n_joint2[1], drop, out_act=False)
    else:
        self.mlp1 = Mlp_JpTrans(n_joint2[0], n_joint2[1], n_joint2[1], drop, out_act=False)
    self.init_weights()
    self.layer1 = layer1
    self.nmp = nmp

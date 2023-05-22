import os
import torch.nn.functional as F
from collections import OrderedDict
from pretrainedmodels import se_resnext50_32x4d, se_resnext101_32x4d
from lib.net.scg_gcn import *


def __init__(self, out_channels=7, pretrained=True, nodes=(32, 32), dropout=0, enhance_diag=True, aux_pred=True):
    super(rx50_gcn_3head_4channel, self).__init__()
    self.aux_pred = aux_pred
    self.node_size = nodes
    self.num_cluster = out_channels
    resnet = se_resnext50_32x4d()
    (self.layer0, self.layer1, self.layer2, self.layer3) = (resnet.layer0, resnet.layer1, resnet.layer2, resnet.layer3)
    self.conv0 = torch.nn.Conv2d(4, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    for child in self.layer0.children():
        for param in child.parameters():
            par = param
            break
        break
    self.conv0.parameters = torch.cat([par[(:, 0, :, :)].unsqueeze(1), par], 1)
    self.layer0 = torch.nn.Sequential(self.conv0, *list(self.layer0)[1:4])
    self.graph_layers1 = GCN_Layer(1024, 128, bnorm=True, activation=nn.ReLU(True), dropout=dropout)
    self.graph_layers2 = GCN_Layer(128, out_channels, bnorm=False, activation=None)
    self.scg = SCG_block(in_ch=1024, hidden_ch=out_channels, node_size=nodes, add_diag=enhance_diag, dropout=dropout)
    weight_xavier_init(self.graph_layers1, self.graph_layers2, self.scg)

import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.aspp import ASPP
from networks.deeplab.backbone.resnet import SEResNet50
from networks.correlation_package.correlation import Correlation
from networks.ltm_transfer import LTM_transfer


def __init__(self):
    super(Decoder_prop, self).__init__()
    mdim = 256
    self.aspp_decoder = ASPP(backbone='res', output_stride=16, BatchNorm=nn.BatchNorm2d, pretrained=1)
    self.convG0 = nn.Conv2d(2048, mdim, kernel_size=3, padding=1)
    self.convG1 = nn.Conv2d(mdim, mdim, kernel_size=3, padding=1)
    self.convG2 = nn.Conv2d(mdim, mdim, kernel_size=3, padding=1)
    self.RF3 = Refine(512, mdim)
    self.RF2 = Refine(256, mdim)
    self.lastconv = nn.Sequential(nn.Conv2d(512, 256, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(256), nn.ReLU(), nn.Dropout(0.5), nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(256), nn.ReLU(), nn.Dropout(0.1), nn.Conv2d(256, 1, kernel_size=1, stride=1))

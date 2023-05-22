import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.resnet import Bottleneck, BasicBlock
from operations import *
from collections import defaultdict
import math
import pdb
import torchvision
import time
from dataset import *
from layers import *
from bi_fpn import BiFPN_PRIMITIVES, BiFPN_Neck_From_Genotype
from layers.box_utils import match_anchors, decode, encode
import numbers
from torchvision.ops import roi_align
from collections import OrderedDict
import logging


def __init__(self, C, num_classes, criterion, phase, search, inter_node=3, args=None, auxiliary_loss=False, searched_fpn_genotype=None, searched_cpm_genotype=None, weight_node=False, weight_channel=False, fusion_multiple=False, with_attention=False, fpn_layers=1, cpm_layers=1, layers=1, residual_learning=False, gumbel_trick=False, **kwargs):
    super(Network, self).__init__()
    self._C = C
    self.num_classes = num_classes
    self._criterion = criterion
    self._inter_node = inter_node
    self.fpn_layers = fpn_layers
    self.cpm_layers = cpm_layers
    self.num_layers = layers
    self.weight_node = weight_node
    self.search = search
    self.cfg = cfg
    self.phase = phase
    self.args = args
    self.auxiliary_loss = auxiliary_loss
    self.gumbel_trick = gumbel_trick
    if self.search:
        raise ValueError('search mode is not supported.')
    self.searched_fpn_genotype = searched_fpn_genotype
    self.searched_cpm_genotype = searched_cpm_genotype
    if cfg['GN']:
        kwargs['norm_layer'] = (lambda x: nn.GroupNorm(num_groups=32, num_channels=x))
    elif cfg['syncBN']:
        kwargs['norm_layer'] = nn.SyncBatchNorm
    else:
        kwargs['norm_layer'] = None
    if (backbone == 'resnet18'):
        try:
            resnet = torchvision.models.resnet18(pretrained=False, **kwargs)
        except Exception as e:
            print(e)
            resnet = torchvision.models.resnet18(pretrained=False, **kwargs)
        fpn_in = [64, 128, 256, 512, 256, 256]
    else:
        raise ValueError('Backbone {} is not supported.'.format(backbone))
    self.layer5 = nn.Sequential(*[BasicConv2d(fpn_in[(- 3)], (fpn_in[(- 3)] // 4), kernel_size=1, stride=1, padding=0), BasicConv2d((fpn_in[(- 3)] // 4), fpn_in[(- 2)], kernel_size=3, stride=2, padding=1)])
    self.layer6 = nn.Sequential(*[BasicConv2d(fpn_in[(- 2)], max((fpn_in[(- 2)] // 4), 128), kernel_size=1, stride=1, padding=0), BasicConv2d(max((fpn_in[(- 2)] // 4), 128), fpn_in[(- 1)], kernel_size=3, stride=2, padding=1)])
    self.stem_layer = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool)
    self.layer1 = nn.Sequential(resnet.layer1)
    self.layer2 = nn.Sequential(resnet.layer2)
    self.layer3 = nn.Sequential(resnet.layer3)
    self.layer4 = nn.Sequential(resnet.layer4)
    self.fpn_in = fpn_in
    cpm_in = ([fpn_cpm_channel] * 6)
    fpn_channel = fpn_cpm_channel
    cpm_channels = fpn_cpm_channel
    output_channels = cpm_in
    self.FPN_CPM()
    self.multibox(output_channels, cfg['mbox'], num_classes)
    if self.search:
        self._initialize_alphas()
    if (self.phase == 'test'):
        self.softmax = nn.Softmax(dim=(- 1))
        self.detect = Detect(num_classes, 0, cfg['num_thresh'], cfg['conf_thresh'], cfg['nms_thresh'])
    self.cfg['feature_maps'] = [[i, i] for i in self.cfg['feature_maps']]
    self.cfg['min_dim'] = [self.cfg['min_dim'], self.cfg['min_dim']]
    if (phase == 'train'):
        if pa:
            self.face_priors = self.init_priors(self.cfg)
            self.head_priors = self.init_priors(self.cfg, min_size=cfg['min_sizes'][:(- 1)], max_size=cfg['max_sizes'][:(- 1)])
            self.body_priors = self.init_priors(self.cfg, min_size=cfg['min_sizes'][:(- 2)], max_size=cfg['max_sizes'][:(- 2)])
        else:
            self.priors = self.init_priors(self.cfg)

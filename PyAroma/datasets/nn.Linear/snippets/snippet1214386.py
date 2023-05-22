import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from modules.utils import *
from modules.losses import *
from modules.backbones import *
from modules.RPN import RegionProposalNet
from libs.roi_pool.roi_pool import roi_pool
from libs.roi_align.roi_align import roi_align


def __init__(self, mode, cfg, logger_handle, **kwargs):
    fasterRCNNBase.__init__(self, FasterRCNNResNets.feature_stride, mode, cfg)
    self.logger_handle = logger_handle
    self.backbone_type = cfg.BACKBONE_TYPE
    self.pretrained_model_path = cfg.PRETRAINED_MODEL_PATH
    self.backbone = ResNets(resnet_type=self.backbone_type, pretrained=False)
    if (mode == 'TRAIN'):
        self.initializeBackbone()
    self.backbone.avgpool = None
    self.backbone.fc = None
    self.base_model = nn.Sequential(*[self.backbone.conv1, self.backbone.bn1, self.backbone.relu, self.backbone.maxpool, self.backbone.layer1, self.backbone.layer2, self.backbone.layer3])
    in_channels = (256 if (self.backbone_type in ['resnet18', 'resnet34']) else 1024)
    self.rpn_net = RegionProposalNet(in_channels=in_channels, feature_stride=self.feature_stride, mode=mode, cfg=cfg)
    self.build_proposal_target_layer = buildProposalTargetLayer(mode, cfg)
    self.top_model = nn.Sequential(*[self.backbone.layer4])
    in_features = (512 if (self.backbone_type in ['resnet18', 'resnet34']) else 2048)
    self.fc_cls = nn.Linear(in_features, self.num_classes)
    if self.is_class_agnostic:
        self.fc_reg = nn.Linear(in_features, 4)
    else:
        self.fc_reg = nn.Linear(in_features, (4 * self.num_classes))
    if (cfg.ADDED_MODULES_WEIGHT_INIT_METHOD and (mode == 'TRAIN')):
        init_methods = cfg.ADDED_MODULES_WEIGHT_INIT_METHOD
        self.rpn_net.initWeights(init_methods['rpn'])
        self.initializeAddedLayers(init_methods['rcnn'])
    if cfg.FIXED_FRONT_BLOCKS:
        for p in self.base_model[0].parameters():
            p.requires_grad = False
        for p in self.base_model[1].parameters():
            p.requires_grad = False
        for p in self.base_model[4].parameters():
            p.requires_grad = False
    self.base_model.apply(fasterRCNNBase.setBnFixed)
    self.top_model.apply(fasterRCNNBase.setBnFixed)

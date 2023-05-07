import torch.nn as nn
from mmcv.cnn.weight_init import normal_init, xavier_init
from mmdet.ops import ConvModule
from ..backbones.resnet import Bottleneck
from ..registry import HEADS
from .bbox_head import BBoxHead


def _add_fc_branch(self):
    'Add the fc branch which consists of a sequential of fc layers'
    branch_fcs = nn.ModuleList()
    for i in range(self.num_fcs):
        fc_in_channels = ((self.in_channels * self.roi_feat_area) if (i == 0) else self.fc_out_channels)
        branch_fcs.append(nn.Linear(fc_in_channels, self.fc_out_channels))
    return branch_fcs

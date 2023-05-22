import torch.nn as nn
from mmdet.ops import ConvModule
from ..registry import HEADS
from .bbox_head import BBoxHead


def _add_conv_fc_branch(self, num_branch_convs, num_branch_fcs, in_channels, is_shared=False):
    'Add shared or separable branch\n\n        convs -> avg pool (optional) -> fcs\n        '
    last_layer_dim = in_channels
    branch_convs = nn.ModuleList()
    if (num_branch_convs > 0):
        for i in range(num_branch_convs):
            conv_in_channels = (last_layer_dim if (i == 0) else self.conv_out_channels)
            branch_convs.append(ConvModule(conv_in_channels, self.conv_out_channels, 3, padding=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg))
        last_layer_dim = self.conv_out_channels
    branch_fcs = nn.ModuleList()
    if (num_branch_fcs > 0):
        if ((is_shared or (self.num_shared_fcs == 0)) and (not self.with_avg_pool)):
            last_layer_dim *= self.roi_feat_area
        for i in range(num_branch_fcs):
            fc_in_channels = (last_layer_dim if (i == 0) else self.fc_out_channels)
            branch_fcs.append(nn.Linear(fc_in_channels, self.fc_out_channels))
        last_layer_dim = self.fc_out_channels
    return (branch_convs, branch_fcs, last_layer_dim)

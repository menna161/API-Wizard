import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import caffe2_xavier_init
from mmdet.ops import ConvModule
from ..registry import NECKS


def __init__(self, in_channels, out_channels, num_outs, stack_times, start_level=0, end_level=(- 1), add_extra_convs=False, norm_cfg=None):
    super(NASFPN, self).__init__()
    assert isinstance(in_channels, list)
    self.in_channels = in_channels
    self.out_channels = out_channels
    self.num_ins = len(in_channels)
    self.num_outs = num_outs
    self.stack_times = stack_times
    self.norm_cfg = norm_cfg
    if (end_level == (- 1)):
        self.backbone_end_level = self.num_ins
        assert (num_outs >= (self.num_ins - start_level))
    else:
        self.backbone_end_level = end_level
        assert (end_level <= len(in_channels))
        assert (num_outs == (end_level - start_level))
    self.start_level = start_level
    self.end_level = end_level
    self.add_extra_convs = add_extra_convs
    self.lateral_convs = nn.ModuleList()
    for i in range(self.start_level, self.backbone_end_level):
        l_conv = ConvModule(in_channels[i], out_channels, 1, norm_cfg=norm_cfg, act_cfg=None)
        self.lateral_convs.append(l_conv)
    extra_levels = ((num_outs - self.backbone_end_level) + self.start_level)
    self.extra_downsamples = nn.ModuleList()
    for i in range(extra_levels):
        extra_conv = ConvModule(out_channels, out_channels, 1, norm_cfg=norm_cfg, act_cfg=None)
        self.extra_downsamples.append(nn.Sequential(extra_conv, nn.MaxPool2d(2, 2)))
    self.fpn_stages = nn.ModuleList()
    for _ in range(self.stack_times):
        stage = nn.ModuleDict()
        stage['gp_64_4'] = GPCell(out_channels, norm_cfg=norm_cfg)
        stage['sum_44_4'] = SumCell(out_channels, norm_cfg=norm_cfg)
        stage['sum_43_3'] = SumCell(out_channels, norm_cfg=norm_cfg)
        stage['sum_34_4'] = SumCell(out_channels, norm_cfg=norm_cfg)
        stage['gp_43_5'] = GPCell(with_conv=False)
        stage['sum_55_5'] = SumCell(out_channels, norm_cfg=norm_cfg)
        stage['gp_54_7'] = GPCell(with_conv=False)
        stage['sum_77_7'] = SumCell(out_channels, norm_cfg=norm_cfg)
        stage['gp_75_6'] = GPCell(out_channels, norm_cfg=norm_cfg)
        self.fpn_stages.append(stage)

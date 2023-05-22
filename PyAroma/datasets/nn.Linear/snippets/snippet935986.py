import torch.nn as nn
from .bbox_head import BBoxHead
from ..registry import HEADS
from ..utils import ConvModule


def init_weights(self):
    super(ConvFCBBoxHead, self).init_weights()
    for module_list in [self.shared_fcs, self.cls_fcs, self.reg_fcs]:
        for m in module_list.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)

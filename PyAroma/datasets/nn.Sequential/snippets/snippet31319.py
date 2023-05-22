import torch.nn as nn
import torch
import util.util as util
from models.shift_net.InnerShiftTripleFunction import InnerShiftTripleFunction


def __init__(self, inner_nc, shift_sz=1, stride=1, mask_thred=1, triple_weight=1, layer_to_last=3):
    super(InnerResShiftTriple, self).__init__()
    self.shift_sz = shift_sz
    self.stride = stride
    self.mask_thred = mask_thred
    self.triple_weight = triple_weight
    self.show_flow = False
    self.flow_srcs = None
    self.layer_to_last = layer_to_last
    self.inner_nc = inner_nc
    self.res_net = nn.Sequential(nn.Conv2d((inner_nc * 2), inner_nc, kernel_size=3, stride=1, padding=1), nn.InstanceNorm2d(inner_nc), nn.ReLU(True), nn.Conv2d(inner_nc, inner_nc, kernel_size=3, stride=1, padding=1), nn.InstanceNorm2d(inner_nc))
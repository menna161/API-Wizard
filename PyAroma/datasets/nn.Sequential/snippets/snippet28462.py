import torch
import torch.nn as nn
from lib.sa.modules import Subtraction, Subtraction2, Aggregation


def __init__(self, sa_type, in_planes, rel_planes, out_planes, share_planes, kernel_size=3, stride=1, dilation=1):
    super(SAM, self).__init__()
    (self.sa_type, self.kernel_size, self.stride) = (sa_type, kernel_size, stride)
    self.conv1 = nn.Conv2d(in_planes, rel_planes, kernel_size=1)
    self.conv2 = nn.Conv2d(in_planes, rel_planes, kernel_size=1)
    self.conv3 = nn.Conv2d(in_planes, out_planes, kernel_size=1)
    if (sa_type == 0):
        self.conv_w = nn.Sequential(nn.BatchNorm2d((rel_planes + 2)), nn.ReLU(inplace=True), nn.Conv2d((rel_planes + 2), rel_planes, kernel_size=1, bias=False), nn.BatchNorm2d(rel_planes), nn.ReLU(inplace=True), nn.Conv2d(rel_planes, (out_planes // share_planes), kernel_size=1))
        self.conv_p = nn.Conv2d(2, 2, kernel_size=1)
        self.subtraction = Subtraction(kernel_size, stride, (((dilation * (kernel_size - 1)) + 1) // 2), dilation, pad_mode=1)
        self.subtraction2 = Subtraction2(kernel_size, stride, (((dilation * (kernel_size - 1)) + 1) // 2), dilation, pad_mode=1)
        self.softmax = nn.Softmax(dim=(- 2))
    else:
        self.conv_w = nn.Sequential(nn.BatchNorm2d((rel_planes * (pow(kernel_size, 2) + 1))), nn.ReLU(inplace=True), nn.Conv2d((rel_planes * (pow(kernel_size, 2) + 1)), (out_planes // share_planes), kernel_size=1, bias=False), nn.BatchNorm2d((out_planes // share_planes)), nn.ReLU(inplace=True), nn.Conv2d((out_planes // share_planes), ((pow(kernel_size, 2) * out_planes) // share_planes), kernel_size=1))
        self.unfold_i = nn.Unfold(kernel_size=1, dilation=dilation, padding=0, stride=stride)
        self.unfold_j = nn.Unfold(kernel_size=kernel_size, dilation=dilation, padding=0, stride=stride)
        self.pad = nn.ReflectionPad2d((kernel_size // 2))
    self.aggregation = Aggregation(kernel_size, stride, (((dilation * (kernel_size - 1)) + 1) // 2), dilation, pad_mode=1)

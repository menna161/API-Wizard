import torch
import torch.nn as nn
import torch.utils.data
from torch.nn import functional as F


def __init__(self, input_nc=6, num_classes=1200, encode_one_hot=True, img_size=128, **kwargs):
    super(Generator, self).__init__()
    self.in_dim = input_nc
    self.encode_one_hot = encode_one_hot
    self.img_size = img_size
    input_ch = input_nc
    if (img_size == 128):
        self.conv0 = ResidualBlockDown(input_ch, 32)
        self.in0_e = nn.InstanceNorm2d(32, affine=True)
        input_ch = 32
    self.conv1 = ResidualBlockDown(input_ch, 64)
    self.in1_e = nn.InstanceNorm2d(64, affine=True)
    self.conv2 = ResidualBlockDown(64, 128)
    self.in2_e = nn.InstanceNorm2d(128, affine=True)
    self.conv3 = ResidualBlockDown(128, 256)
    self.in3_e = nn.InstanceNorm2d(256, affine=True)
    self.conv4 = ResidualBlockDown(256, 256)
    self.in4_e = nn.InstanceNorm2d(256, affine=True)
    self.embed = nn.Sequential(ConvLayer(512, 256, kernel_size=3, stride=1), nn.InstanceNorm2d(256, affine=True))
    self.res1 = ResidualBlock(256)
    self.res2 = ResidualBlock(256)
    self.res3 = ResidualBlock(256)
    self.res4 = ResidualBlock(256)
    self.deconv4 = ResidualBlockUp(256, 256, upsample=2)
    self.in4_d = nn.InstanceNorm2d(256, affine=True)
    self.deconv3 = ResidualBlockUp(256, 128, upsample=2)
    self.in3_d = nn.InstanceNorm2d(128, affine=True)
    self.deconv2 = ResidualBlockUp(128, 64, upsample=2)
    self.in2_d = nn.InstanceNorm2d(64, affine=True)
    self.deconv1 = ResidualBlockUp(64, 32, upsample=2)
    self.in1_d = nn.InstanceNorm2d(32, affine=True)
    if (img_size == 128):
        self.deconv0 = ResidualBlockUp(32, 16, upsample=2)
        self.in0_d = nn.InstanceNorm2d(16, affine=True)
    self.conv_end = nn.Sequential(nn.Conv2d(16, 3, kernel_size=3, stride=1, padding=1))
    self.flag_onehot = encode_one_hot
    if encode_one_hot:
        self.encode_one_hot = nn.Sequential(nn.Linear(num_classes, 256), nn.LeakyReLU(0.2, inplace=True), nn.Linear(256, 256), nn.LeakyReLU(0.2, inplace=True), nn.Linear(256, 256), nn.LeakyReLU(0.2, inplace=True), nn.Linear(256, 256), nn.LeakyReLU(0.2, inplace=True), nn.Linear(256, 512), nn.LeakyReLU(0.2, inplace=True), nn.Linear(512, 512), nn.LeakyReLU(0.2, inplace=True), nn.Linear(512, 512), nn.LeakyReLU(0.2, inplace=True))
        self.encode_noise = nn.Sequential(ConvLayer(32, 64, kernel_size=3, stride=1), nn.LeakyReLU(0.2, inplace=True), nn.InstanceNorm2d(64, affine=True), ConvLayer(64, 128, kernel_size=3, stride=1), nn.LeakyReLU(0.2, inplace=True), nn.InstanceNorm2d(128, affine=True), ConvLayer(128, 256, kernel_size=3, stride=1), nn.LeakyReLU(0.2, inplace=True), nn.InstanceNorm2d(256, affine=True))
    else:
        self.encode_one_hot = None

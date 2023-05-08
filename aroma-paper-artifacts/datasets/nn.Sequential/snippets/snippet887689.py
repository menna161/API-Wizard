import os
import torch.nn as nn
import torch.optim as optim
from base_networks import *
from torchvision.transforms import *


def __init__(self, num_channels, base_filter, image_size):
    super(Discriminator, self).__init__()
    self.image_size = image_size
    self.input_conv = ConvBlock(num_channels, base_filter, 3, 1, 1, activation='lrelu', norm=None)
    self.conv_blocks = nn.Sequential(ConvBlock(base_filter, base_filter, 3, 2, 1, activation='lrelu', norm='batch'), ConvBlock(base_filter, (base_filter * 2), 3, 1, 1, activation='lrelu', norm='batch'), ConvBlock((base_filter * 2), (base_filter * 2), 3, 2, 1, activation='lrelu', norm='batch'), ConvBlock((base_filter * 2), (base_filter * 4), 3, 1, 1, activation='lrelu', norm='batch'), ConvBlock((base_filter * 4), (base_filter * 4), 3, 2, 1, activation='lrelu', norm='batch'), ConvBlock((base_filter * 4), (base_filter * 8), 3, 1, 1, activation='lrelu', norm='batch'), ConvBlock((base_filter * 8), (base_filter * 8), 3, 2, 1, activation='lrelu', norm='batch'))
    self.dense_layers = nn.Sequential(DenseBlock((((((base_filter * 8) * image_size) // 16) * image_size) // 16), (base_filter * 16), activation='lrelu', norm=None), DenseBlock((base_filter * 16), 1, activation='sigmoid', norm=None))
    for m in self.modules():
        classname = m.__class__.__name__
        if (classname.find('Conv2d') != (- 1)):
            torch.nn.init.kaiming_normal_(m.weight)
            if (m.bias is not None):
                m.bias.data.zero_()
        elif (classname.find('ConvTranspose2d') != (- 1)):
            torch.nn.init.kaiming_normal_(m.weight)
            if (m.bias is not None):
                m.bias.data.zero_()

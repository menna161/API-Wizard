import torch
import math


def __init__(self, input_size, output_size, bias=True, upsample='deconv', activation='relu', norm='batch'):
    super(Upsample2xBlock, self).__init__()
    scale_factor = 2
    if (upsample == 'deconv'):
        self.upsample = DeconvBlock(input_size, output_size, kernel_size=4, stride=2, padding=1, bias=bias, activation=activation, norm=norm)
    elif (upsample == 'ps'):
        self.upsample = PSBlock(input_size, output_size, scale_factor=scale_factor, bias=bias, activation=activation, norm=norm)
    elif (upsample == 'rnc'):
        self.upsample = torch.nn.Sequential(torch.nn.Upsample(scale_factor=scale_factor, mode='nearest'), ConvBlock(input_size, output_size, kernel_size=3, stride=1, padding=1, bias=bias, activation=activation, norm=norm))

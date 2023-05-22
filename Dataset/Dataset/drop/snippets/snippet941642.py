import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from .vgg import Vgg19
import math
import cv2
import numpy as np
import scipy.stats as st
import code


def define_G(input_nc, output_nc, ngf, netG, norm='batch', use_dropout=False, init_type='normal', init_gain=0.02, gpu_ids=[]):
    "Create a generator\n\n    Parameters:\n        input_nc (int) -- the number of channels in input images\n        output_nc (int) -- the number of channels in output images\n        ngf (int) -- the number of filters in the last conv layer\n        netG (str) -- the architecture's name: resnet_9blocks | resnet_6blocks | unet_256 | unet_128\n        norm (str) -- the name of normalization layers used in the network: batch | instance | none\n        use_dropout (bool) -- if use dropout layers.\n        init_type (str)    -- the name of our initialization method.\n        init_gain (float)  -- scaling factor for normal, xavier and orthogonal.\n        gpu_ids (int list) -- which GPUs the network runs on: e.g., 0,1,2\n\n    Returns a generator\n\n    Our current implementation provides two types of generators:\n        U-Net: [unet_128] (for 128x128 input images) and [unet_256] (for 256x256 input images)\n        The original U-Net paper: https://arxiv.org/abs/1505.04597\n\n        Resnet-based generator: [resnet_6blocks] (with 6 Resnet blocks) and [resnet_9blocks] (with 9 Resnet blocks)\n        Resnet-based generator consists of several Resnet blocks between a few downsampling/upsampling operations.\n        We adapt Torch code from Justin Johnson's neural style transfer project (https://github.com/jcjohnson/fast-neural-style).\n\n\n    The generator has been initialized by <init_net>. It uses RELU for non-linearity.\n    "
    net = None
    norm_layer = get_norm_layer(norm_type=norm)
    if (netG == 'resnet_9blocks'):
        net = ResnetGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=9)
    elif (netG == 'resnet_6blocks'):
        net = ResnetGenerator(input_nc, output_nc, ngf, norm_layer=norm_layer, use_dropout=use_dropout, n_blocks=6)
    elif (netG == 'unet_128'):
        net = UnetGenerator(input_nc, output_nc, 7, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif (netG == 'unet_256'):
        net = UnetGenerator(input_nc, output_nc, 8, ngf, norm_layer=norm_layer, use_dropout=use_dropout)
    elif (netG == 'gen_drop'):
        net = Generator_drop(input_nc, output_nc, ngf)
    else:
        raise NotImplementedError(('Generator model name [%s] is not recognized' % netG))
    return init_net(net, init_type, init_gain, gpu_ids)

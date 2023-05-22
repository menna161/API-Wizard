import numpy as np
import torch
from nnunet.network_architecture.custom_modules.conv_blocks import BasicResidualBlock, ResidualLayer
from nnunet.network_architecture.generic_UNet import Upsample
from nnunet.network_architecture.generic_modular_UNet import PlainConvUNetDecoder, get_default_network_config
from nnunet.network_architecture.neural_network import SegmentationNetwork
from nnunet.training.loss_functions.dice_loss import DC_and_CE_loss
from torch import nn
from torch.optim import SGD
from torch.backends import cudnn


def __init__(self, previous, num_classes, num_blocks_per_stage=None, network_props=None, deep_supervision=False, upscale_logits=False, block=BasicResidualBlock):
    super(ResidualUNetDecoder, self).__init__()
    self.num_classes = num_classes
    self.deep_supervision = deep_supervision
    '\n        We assume the bottleneck is part of the encoder, so we can start with upsample -> concat here\n        '
    previous_stages = previous.stages
    previous_stage_output_features = previous.stage_output_features
    previous_stage_pool_kernel_size = previous.stage_pool_kernel_size
    previous_stage_conv_op_kernel_size = previous.stage_conv_op_kernel_size
    if (network_props is None):
        self.props = previous.props
    else:
        self.props = network_props
    if (self.props['conv_op'] == nn.Conv2d):
        transpconv = nn.ConvTranspose2d
        upsample_mode = 'bilinear'
    elif (self.props['conv_op'] == nn.Conv3d):
        transpconv = nn.ConvTranspose3d
        upsample_mode = 'trilinear'
    else:
        raise ValueError(('unknown convolution dimensionality, conv op: %s' % str(self.props['conv_op'])))
    if (num_blocks_per_stage is None):
        num_blocks_per_stage = previous.num_blocks_per_stage[:(- 1)][::(- 1)]
    assert (len(num_blocks_per_stage) == (len(previous.num_blocks_per_stage) - 1))
    self.stage_pool_kernel_size = previous_stage_pool_kernel_size
    self.stage_output_features = previous_stage_output_features
    self.stage_conv_op_kernel_size = previous_stage_conv_op_kernel_size
    num_stages = (len(previous_stages) - 1)
    self.tus = []
    self.stages = []
    self.deep_supervision_outputs = []
    cum_upsample = np.cumprod(np.vstack(self.stage_pool_kernel_size), axis=0).astype(int)
    for (i, s) in enumerate(np.arange(num_stages)[::(- 1)]):
        features_below = previous_stage_output_features[(s + 1)]
        features_skip = previous_stage_output_features[s]
        self.tus.append(transpconv(features_below, features_skip, previous_stage_pool_kernel_size[(s + 1)], previous_stage_pool_kernel_size[(s + 1)], bias=False))
        self.stages.append(ResidualLayer((2 * features_skip), features_skip, previous_stage_conv_op_kernel_size[s], self.props, num_blocks_per_stage[i], None, block))
        if (deep_supervision and (s != 0)):
            seg_layer = self.props['conv_op'](features_skip, num_classes, 1, 1, 0, 1, 1, False)
            if upscale_logits:
                upsample = Upsample(scale_factor=cum_upsample[s], mode=upsample_mode)
                self.deep_supervision_outputs.append(nn.Sequential(seg_layer, upsample))
            else:
                self.deep_supervision_outputs.append(seg_layer)
    self.segmentation_output = self.props['conv_op'](features_skip, num_classes, 1, 1, 0, 1, 1, False)
    self.tus = nn.ModuleList(self.tus)
    self.stages = nn.ModuleList(self.stages)
    self.deep_supervision_outputs = nn.ModuleList(self.deep_supervision_outputs)

from copy import deepcopy
from nnunet.utilities.nd_softmax import softmax_helper
from torch import nn
import torch
import numpy as np
from nnunet.network_architecture.initialization import InitWeights_He
from nnunet.network_architecture.neural_network import SegmentationNetwork
import torch.nn.functional


def __init__(self, input_feature_channels, output_feature_channels, num_convs, conv_op=nn.Conv2d, conv_kwargs=None, norm_op=nn.BatchNorm2d, norm_op_kwargs=None, dropout_op=nn.Dropout2d, dropout_op_kwargs=None, nonlin=nn.LeakyReLU, nonlin_kwargs=None, first_stride=None, basic_block=ConvDropoutNormNonlin):
    '\n        stacks ConvDropoutNormLReLU layers. initial_stride will only be applied to first layer in the stack. The other parameters affect all layers\n        :param input_feature_channels:\n        :param output_feature_channels:\n        :param num_convs:\n        :param dilation:\n        :param kernel_size:\n        :param padding:\n        :param dropout:\n        :param initial_stride:\n        :param conv_op:\n        :param norm_op:\n        :param dropout_op:\n        :param inplace:\n        :param neg_slope:\n        :param norm_affine:\n        :param conv_bias:\n        '
    self.input_channels = input_feature_channels
    self.output_channels = output_feature_channels
    if (nonlin_kwargs is None):
        nonlin_kwargs = {'negative_slope': 0.01, 'inplace': True}
    if (dropout_op_kwargs is None):
        dropout_op_kwargs = {'p': 0.5, 'inplace': True}
    if (norm_op_kwargs is None):
        norm_op_kwargs = {'eps': 1e-05, 'affine': True, 'momentum': 0.1}
    if (conv_kwargs is None):
        conv_kwargs = {'kernel_size': 3, 'stride': 1, 'padding': 1, 'dilation': 1, 'bias': True}
    self.nonlin_kwargs = nonlin_kwargs
    self.nonlin = nonlin
    self.dropout_op = dropout_op
    self.dropout_op_kwargs = dropout_op_kwargs
    self.norm_op_kwargs = norm_op_kwargs
    self.conv_kwargs = conv_kwargs
    self.conv_op = conv_op
    self.norm_op = norm_op
    if (first_stride is not None):
        self.conv_kwargs_first_conv = deepcopy(conv_kwargs)
        self.conv_kwargs_first_conv['stride'] = first_stride
    else:
        self.conv_kwargs_first_conv = conv_kwargs
    super(StackedConvLayers, self).__init__()
    self.blocks = nn.Sequential(*([basic_block(input_feature_channels, output_feature_channels, self.conv_op, self.conv_kwargs_first_conv, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs)] + [basic_block(output_feature_channels, output_feature_channels, self.conv_op, self.conv_kwargs, self.norm_op, self.norm_op_kwargs, self.dropout_op, self.dropout_op_kwargs, self.nonlin, self.nonlin_kwargs) for _ in range((num_convs - 1))]))

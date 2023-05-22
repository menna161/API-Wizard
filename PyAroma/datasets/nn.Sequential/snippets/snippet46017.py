import numpy as np
import torch
import torch.nn as nn
import probabilistic_pac


def __init__(self, kernel_size_preprocessing, kernel_size_joint, conv_specification, shared_filters, depth_layers_prob, depth_layers_guidance, depth_layers_joint, fixed_gaussian_weights=False, bias_zero_init=False):
    super(PPacNet, self).__init__()
    self.conv_specification = conv_specification
    self.depth_layers_joint = depth_layers_joint
    num_pac = conv_specification.count('p')
    assert (depth_layers_prob[(- 1)] == num_pac)
    self.guidance_share = int((depth_layers_guidance[(- 1)] / num_pac))
    assert ((self.guidance_share * num_pac) == depth_layers_guidance[(- 1)])
    layers_guidance = []
    for i in range(1, len(depth_layers_guidance)):
        layers_guidance.append(nn.Conv2d(depth_layers_guidance[(i - 1)], depth_layers_guidance[i], kernel_size=kernel_size_preprocessing, stride=1, padding=(kernel_size_preprocessing // 2), dilation=1, bias=True))
        if (i < (len(depth_layers_guidance) - 1)):
            layers_guidance.append(nn.ReLU(inplace=True))
    self.network_guidance = nn.Sequential(*layers_guidance)
    layers_prob = []
    for i in range(1, len(depth_layers_prob)):
        layers_prob.append(nn.Conv2d(depth_layers_prob[(i - 1)], depth_layers_prob[i], kernel_size=kernel_size_preprocessing, stride=1, padding=(kernel_size_preprocessing // 2), dilation=1, bias=True))
        if (i < (len(depth_layers_prob) - 1)):
            layers_prob.append(nn.ReLU(inplace=True))
    self.network_prob = nn.Sequential(*layers_prob)
    layers_joint = nn.ModuleList()
    for (i, conv_type) in enumerate(conv_specification):
        if (conv_type == 'p'):
            layers_joint.append(probabilistic_pac.ProbPacConv2d(depth_layers_joint[i], depth_layers_joint[(i + 1)], kernel_size_joint, padding=(kernel_size_joint // 2), bias=True, kernel_type='gaussian', shared_filters=shared_filters))
        elif (conv_type == 'c'):
            layers_joint.append(nn.Conv2d(depth_layers_joint[i], depth_layers_joint[(i + 1)], kernel_size=kernel_size_joint, stride=1, padding=(kernel_size_joint // 2), dilation=1, bias=True))
        else:
            raise ValueError('Unknown convolution type {}'.format(type))
    self.layers_joint = layers_joint
    if bias_zero_init:
        for layer in self.layers_joint:
            torch.nn.init.zeros_(layer.bias)
    if fixed_gaussian_weights:
        for layer in self.layers_joint:
            layer.weight.requires_grad = False
            layer.weight.data = gaussian_kernel(kernel_size=kernel_size_joint, sigma=1.0)
            layer.weight_normalization.data = torch.log(gaussian_kernel(kernel_size=kernel_size_joint, sigma=1.0))
            layer.weight_normalization.requires_grad = False
            layer.bias.requires_grad = False

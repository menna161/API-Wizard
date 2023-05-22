from __future__ import annotations
import math
from typing import TYPE_CHECKING
import torch
import torch.nn as nn
from agent.model.modules import convolution_layer
from agent.model.modules import inverse_convolution_layer
from agent.config import state_encoder_args
from typing import List, Optional, Tuple


def __init__(self, args: state_encoder_args.StateEncoderArgs, input_channels: int, text_hidden_size: int, output_channels: int, dropout: float=0.0, extra_head_channels: int=0, input_img_size: int=0, layer_single_preds: bool=False):
    super(LingUNet, self).__init__()
    self._args: state_encoder_args.StateEncoderArgs = args
    self._input_channels: int = input_channels
    depth: int = self._args.get_encoder_depth()
    if ((text_hidden_size % depth) != 0):
        raise ValueError(((('Text hidden size should be evenly divisible by depth: ' + str(text_hidden_size)) + ' vs. ') + str(depth)))
    sliced_text_vector_size: int = (text_hidden_size // depth)
    self._convolution_layers = nn.ModuleList([])
    self._text_kernel_fully_connected = nn.ModuleList([])
    self._text_convolution_instance_normsl = nn.ModuleList([])
    self._inverse_convolution_layers = nn.ModuleList([])
    self._text_kernel_outsizes: List[Tuple[(int, int)]] = list()
    self._dropout_layer = nn.Dropout(dropout)
    self._layer_single_preds: bool = layer_single_preds
    self._single_pred_layers = nn.ModuleList([])
    self._top_text_single_pred = None
    for i in range(depth):
        conv_in_channels = (self._args.get_lingunet_after_convolution_channels() if (i > 0) else input_channels)
        conv_out_channels: int = self._args.get_lingunet_after_convolution_channels()
        conv_module = nn.ModuleList([])
        conv_module.append(convolution_layer.ConvolutionLayer(self._args.get_lingunet_convolution_layers(), conv_in_channels, conv_out_channels, kernel_size=self._args.get_kernel_size(), stride=self._args.get_encoder_stride(), padding=self._args.get_encoder_padding(), initializer=self._args.get_vpn_convolution_initialization()))
        if self._args.lingunet_nonlinearities():
            conv_module.append(nn.LeakyReLU())
        if ((i < (depth - 1)) and self._args.lingunet_normalize()):
            conv_module.append(nn.InstanceNorm2d(conv_out_channels))
        self._convolution_layers.append(conv_module)
        text_out_channels: int = (self._args.get_lingunet_after_text_channels() if (i < (depth - 1)) else conv_out_channels)
        self._text_kernel_fully_connected.append(nn.Linear(sliced_text_vector_size, (conv_out_channels * text_out_channels)))
        self._text_kernel_outsizes.append((text_out_channels, conv_out_channels))
        if ((i < (depth - 1)) and self._args.lingunet_normalize()):
            self._text_convolution_instance_normsl.append(nn.InstanceNorm2d(text_out_channels))
        if (self._layer_single_preds and (i == 0)):
            self._top_text_single_pred = nn.Conv2d(text_out_channels, 1, 1, bias=False)
            self._args.get_vpn_convolution_initialization().initialize(self._top_text_single_pred.weight)
        if (i > 0):
            deconv_in_channels = (text_out_channels if (i == (depth - 1)) else (text_out_channels + conv_out_channels))
            deconv_out_channels = (conv_out_channels if (i > 1) else input_channels)
            deconv_module = nn.ModuleList([])
            deconv_module.append(inverse_convolution_layer.InverseConvolutionLayer(self._args.get_lingunet_convolution_layers(), deconv_in_channels, deconv_out_channels, kernel_size=self._args.get_kernel_size(), stride=self._args.get_encoder_stride(), padding=self._args.get_encoder_padding(), initializer=self._args.get_vpn_convolution_initialization(), upsampling_deconv=False))
            if self._args.lingunet_nonlinearities():
                deconv_module.append(nn.LeakyReLU())
            if ((i < (depth - 1)) and self._args.lingunet_normalize()):
                deconv_module.append(nn.InstanceNorm2d(deconv_out_channels))
            self._inverse_convolution_layers.append(deconv_module)
            if self._layer_single_preds:
                map_conv: nn.Module = nn.Conv2d(deconv_out_channels, 1, 1, bias=False)
                self._args.get_vpn_convolution_initialization().initialize(map_conv.weight)
                self._single_pred_layers.append(map_conv)
    input_to_deconv_size = (input_channels + self._text_kernel_outsizes[0][0])
    out_size = (output_channels if (self._args.get_vpn_num_output_hidden_layers() == 0) else input_to_deconv_size)
    self._final_deconv = nn.ConvTranspose2d(input_to_deconv_size, out_size, kernel_size=self._args.get_kernel_size(), stride=self._args.get_encoder_stride(), padding=self._args.get_encoder_padding())
    self._final_mlps = None
    if (self._args.get_vpn_num_output_hidden_layers() > 0):
        hidden_layers = []
        for i in range((self._args.get_vpn_num_output_hidden_layers() - 1)):
            hidden_layers += [nn.Linear(input_to_deconv_size, input_to_deconv_size), nn.ReLU()]
        self._final_mlps = nn.Sequential(*hidden_layers, nn.Linear(input_to_deconv_size, 1, bias=False))
    self._second_head_conv: nn.Module = None
    self._second_head_maxpool: nn.Module = None
    if extra_head_channels:
        if (input_img_size <= 0):
            raise ValueError('Input image size should be provided when expecting extra outputs.')
        self._second_head_conv = nn.Conv2d(input_to_deconv_size, extra_head_channels, self._args.get_kernel_size(), stride=self._args.get_encoder_stride())
        self._args.get_vpn_convolution_initialization().initialize(self._second_head_conv.weight)
        second_head_conv_stride: int = math.ceil((math.ceil((input_img_size / self._args.get_encoder_stride())) / self._args.get_encoder_stride()))
        self._second_head_maxpool = nn.MaxPool2d(second_head_conv_stride)

import torch
from torch import nn
from torch.nn import functional as F
from functools import partial
from .utils import round_filters, round_repeats, drop_connect, get_same_padding_conv2d, get_model_params, efficientnet_params, load_pretrained_weights, MemoryEfficientSwish


def __init__(self, blocks_args=None, global_params=None, norm_layer=None):
    super().__init__()
    assert isinstance(blocks_args, list), 'blocks_args should be a list'
    assert (len(blocks_args) > 0), 'block args must be greater than 0'
    self._global_params = global_params
    self._blocks_args = blocks_args
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    Conv2d = get_same_padding_conv2d(image_size=global_params.image_size)
    bn_mom = (1 - self._global_params.batch_norm_momentum)
    bn_eps = self._global_params.batch_norm_epsilon
    in_channels = 3
    out_channels = round_filters(32, self._global_params)
    self._conv_stem = Conv2d(in_channels, out_channels, kernel_size=3, stride=2, bias=False)
    self._bn0 = norm_layer(num_features=out_channels, momentum=bn_mom, eps=bn_eps)
    self._blocks = nn.ModuleList([])
    for (idx, block_args) in enumerate(self._blocks_args):
        block_args = block_args._replace(input_filters=round_filters(block_args.input_filters, self._global_params), output_filters=round_filters(block_args.output_filters, self._global_params), num_repeat=round_repeats(block_args.num_repeat, self._global_params))
        self._blocks.append(MBConvBlock(block_args, self._global_params, norm_layer=norm_layer))
        if (block_args.num_repeat > 1):
            block_args = block_args._replace(input_filters=block_args.output_filters, stride=1)
        for _ in range((block_args.num_repeat - 1)):
            self._blocks.append(MBConvBlock(block_args, self._global_params, norm_layer=norm_layer))
    in_channels = block_args.output_filters
    out_channels = round_filters(1280, self._global_params)
    self._conv_head = Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
    self._bn1 = norm_layer(num_features=out_channels, momentum=bn_mom, eps=bn_eps)
    self._avg_pooling = nn.AdaptiveAvgPool2d(1)
    self._dropout = nn.Dropout(self._global_params.dropout_rate)
    self._fc = nn.Linear(out_channels, self._global_params.num_classes)
    self._swish = MemoryEfficientSwish()

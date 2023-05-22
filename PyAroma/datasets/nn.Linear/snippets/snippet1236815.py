from __future__ import annotations
from typing import TYPE_CHECKING
import math
import torch
import torch.nn as nn
from agent.model.map_transformations import map_transformer
from agent.model.map_transformations import pose
from agent.environment import util as environment_util


def __init__(self, input_num_channels: int, internal_size: int, output_size: int, crop_size: int, use_convolution: bool, final_nonlinearity: bool):
    super(MapDistributionEmbedder, self).__init__()
    self._current_position_transformer: map_transformer.MapTransformer = map_transformer.MapTransformer(source_map_size=environment_util.ENVIRONMENT_WIDTH, dest_map_size=environment_util.PADDED_WIDTH, world_size_px=environment_util.ENVIRONMENT_WIDTH, world_size_m=environment_util.ENVIRONMENT_WIDTH)
    if (torch.cuda.device_count() >= 1):
        self._current_position_transformer = self._current_position_transformer.cuda()
    self._final_nonlinearity = final_nonlinearity
    self._convolution_layer = None
    linear_in_size = ((input_num_channels * crop_size) * crop_size)
    if use_convolution:
        self._convolution_layer = nn.Conv2d(input_num_channels, (2 * input_num_channels), kernel_size=3, padding=1, stride=2, bias=True)
        self._convolution_activation = nn.LeakyReLU()
        self._convolution_normalization = nn.InstanceNorm2d((2 * input_num_channels))
        linear_in_size = int((((2 * input_num_channels) * math.ceil((crop_size / 2))) * math.ceil((crop_size / 2))))
    self._state_embedding_layer_1: nn.Module = nn.Linear(linear_in_size, internal_size)
    torch.nn.init.orthogonal_(self._state_embedding_layer_1.weight, torch.nn.init.calculate_gain('leaky_relu'))
    self._state_embedding_layer_1.bias.data.fill_(0)
    self._nonlinearity: nn.Module = nn.LeakyReLU()
    self._state_embedding_layer_2: nn.Module = nn.Linear((internal_size + linear_in_size), output_size)
    torch.nn.init.orthogonal_(self._state_embedding_layer_2.weight, torch.nn.init.calculate_gain('leaky_relu'))
    self._state_embedding_layer_2.bias.data.fill_(0)
    self._crop_size: int = crop_size

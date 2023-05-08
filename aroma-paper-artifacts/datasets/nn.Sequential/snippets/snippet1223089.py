import torch
from torch import nn
from dataclasses import dataclass
from networks.blocks import ConvBNNonLinear, RepeatedInvertedResidual
from networks.blocks import GlobalAvgPool2d
from networks import layers
from networks.layers.non_linear import NonLinearType


def __init__(self, nc, input_channels=3, n_classes=1000, stage_config=DEFAULT_CONFIG, survival_prob=0.8, se_ratio=0.25, p_drop_out=0.2, nl_type=NonLinearType.SWISH, batch_norm_epsilon=0.001, batch_norm_momentum=0.01):
    '\n        The init function of the EfficientNet Module\n\n        :param nc: Network controller\n        :param input_channels: Input number channels\n        :param n_classes: the number of output classes\n        :param stage_config: A list of Stage configs\n        :param survival_prob: The stochastic depth survival probability\n        :param se_ratio: The ratio of the Squeeze Excite block\n        :param p_drop_out: The dropout probability\n        :param nl_type: The non-linear function type\n        :param batch_norm_epsilon: The batch normalization epsilon value\n        :param batch_norm_momentum: The batch normalization momentum value\n        '
    super(EfficientNet, self).__init__()
    blocks_list = []
    n_channels = input_channels
    base_drop_rate = (1.0 - survival_prob)
    n_blocks = sum([(sc.stem * sc.n_repeat) for sc in stage_config])
    drop_rate = (base_drop_rate / n_blocks)
    past_index = 0
    for (i, sc) in enumerate(stage_config):
        if sc.stem:
            blocks_list.append(ConvBNNonLinear(nc, n_channels, sc.output_channels, kernel_size=sc.kernel_size, stride=sc.stride_first, nl_type=nl_type, batch_norm_epsilon=batch_norm_epsilon, batch_norm_momentum=batch_norm_momentum, tf_padding=True))
        else:
            survival_prob_start = (1.0 - (drop_rate * past_index))
            blocks_list.append(RepeatedInvertedResidual(nc, sc.n_repeat, n_channels, sc.output_channels, sc.stride_first, expand_ratio=sc.expand_ratio, kernel_size=sc.kernel_size, nl_type=nl_type, se_ratio=se_ratio, survival_prob_start=survival_prob_start, drop_rate=drop_rate, batch_norm_epsilon=batch_norm_epsilon, tf_padding=True))
            past_index += sc.n_repeat
        n_channels = sc.output_channels
    self.conv_blocks = nn.Sequential(*blocks_list)
    self.conv_blocks_list = blocks_list
    self.conv_head = ConvBNNonLinear(nc, n_channels, 1280, kernel_size=1, nl_type=nl_type, batch_norm_epsilon=batch_norm_epsilon)
    self.gap = GlobalAvgPool2d()
    self.drop_out = nn.Dropout(p=p_drop_out)
    self.fc = layers.FullyConnected(nc, 1280, n_classes)

import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.uniform import Uniform
from networks.layers.non_linear import NonLinear, NonLinearType
from networks.layers.conv_bn import ConvBN


def __init__(self, nc, n_repeat, in_channels, out_channels, stride_first, expand_ratio, kernel_size=3, nl_type=NonLinearType.RELU6, se_ratio=0, survival_prob_start=0, drop_rate=0, batch_norm_epsilon=1e-05, batch_norm_momentum=0.1, tf_padding=False):
    '\n        A block the repeatedly run the InvertedResidual block\n        :param nc:The network quantization controller\n        :param n_repeat:\n        :param in_channels: The number of input channels\n        :param out_channels: The number of output channels\n        :param stride_first: The depth wise convolution stride in the first block\n        :param expand_ratio: The block expand ratio for depth-wise convolution\n        :param kernel_size: The kernel size\n        :param nl_type:  enum that state the non-linear type.\n        :param se_ratio: the ratio between the number of input channel and mid channels in SE Bloock\n        :param survival_prob_start: the probability if connection survival in the first block\n        :param batch_norm_epsilon: The batch normalization epsilon\n        :param batch_norm_momentum: The batch normalization momentum\n        :param tf_padding: Use TensorFlow padding (for EfficientNet)\n        '
    super(RepeatedInvertedResidual, self).__init__()
    layers = []
    for i in range(n_repeat):
        if ((survival_prob_start > 0) and (drop_rate > 0)):
            survival_prob = (survival_prob_start - (drop_rate * float(i)))
        else:
            survival_prob = 0
        block = InvertedResidual(nc, (in_channels if (i == 0) else out_channels), out_channels, (stride_first if (i == 0) else 1), expand_ratio, kernel_size=kernel_size, nl_type=nl_type, se_ratio=se_ratio, survival_prob=survival_prob, batch_norm_epsilon=batch_norm_epsilon, batch_norm_momentum=batch_norm_momentum, tf_padding=tf_padding)
        layers.append(block)
    self.blocks = nn.Sequential(*layers)

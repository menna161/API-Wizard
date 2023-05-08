import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.uniform import Uniform
from networks.layers.non_linear import NonLinear, NonLinearType
from networks.layers.conv_bn import ConvBN


def __init__(self, nc, inp, oup, stride, expand_ratio, kernel_size=3, nl_type=NonLinearType.RELU6, se_ratio=0, survival_prob=0, batch_norm_epsilon=1e-05, batch_norm_momentum=0.1, tf_padding=False):
    '\n        A Inverted Residual block use in Efficient-Net\n\n        :param nc: The network quantization controller\n        :param inp: The number of input channels\n        :param oup: The number of output channels\n        :param stride: The depth wise convolution stride\n        :param expand_ratio: The block expand ratio for depth-wise convolution\n        :param kernel_size: The kernel size\n        :param nl_type:  enum that state the non-linear type.\n        :param se_ratio: the ratio between the number of input channel and mid channels in SE Bloock\n        :param survival_prob: the probability if connection survival\n        :param batch_norm_epsilon: The batch normalization epsilon\n        :param batch_norm_momentum: The batch normalization momentum\n        :param tf_padding: Use TensorFlow padding (for EfficientNet)\n        '
    super(InvertedResidual, self).__init__()
    self.stride = stride
    assert (stride in [1, 2])
    hidden_dim = int(round((inp * expand_ratio)))
    self.use_res_connect = ((self.stride == 1) and (inp == oup))
    self.kernel_size = kernel_size
    layers = []
    if (expand_ratio != 1):
        layers.append(ConvBNNonLinear(nc, inp, hidden_dim, kernel_size=1, nl_type=nl_type, batch_norm_epsilon=batch_norm_epsilon, batch_norm_momentum=batch_norm_momentum))
    layers.append(ConvBNNonLinear(nc, hidden_dim, hidden_dim, kernel_size=kernel_size, stride=stride, groups=hidden_dim, nl_type=nl_type, batch_norm_epsilon=batch_norm_epsilon, batch_norm_momentum=batch_norm_momentum, tf_padding=tf_padding))
    if (se_ratio != 0):
        layers.append(SEBlock(nc, hidden_dim, int((inp * se_ratio))))
    layers.append(ConvBNNonLinear(nc, hidden_dim, oup, kernel_size=1, stride=1, nl_type=NonLinearType.IDENTITY, batch_norm_epsilon=batch_norm_epsilon, batch_norm_momentum=batch_norm_momentum))
    if ((survival_prob != 0) and self.use_res_connect):
        layers.append(DropConnect(survival_prob))
    self.conv = nn.Sequential(*layers)
    self.output_q = NonLinear(nc, oup, nl_type=NonLinearType.IDENTITY)

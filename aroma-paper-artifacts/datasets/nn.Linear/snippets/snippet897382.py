import torch
from torch import nn
from torch.autograd import Function
import torch.nn.functional as F
import dynamicconv_cuda
from fairseq import utils
from fairseq.modules.unfold import unfold1d


def __init__(self, input_size, kernel_size=1, padding_l=None, weight_softmax=False, num_heads=1, weight_dropout=0.0, bias=False, renorm_padding=False, conv_bias=False, query_size=None):
    super(DynamicconvLayer, self).__init__()
    self.input_size = input_size
    self.query_size = (input_size if (query_size is None) else query_size)
    self.kernel_size = kernel_size
    self.padding_l = padding_l
    self.num_heads = num_heads
    self.weight_softmax = weight_softmax
    self.weight_dropout = weight_dropout
    self.renorm_padding = renorm_padding
    self.bias = bias
    self.weight_linear = nn.Linear(input_size, (num_heads * kernel_size), bias)
    if conv_bias:
        self.conv_bias = nn.Parameter(torch.Tensor(input_size))
    else:
        self.conv_bias = None
    self.reset_parameters()

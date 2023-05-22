from typing import Dict, Iterator, List, Tuple
from collections import OrderedDict
import torch
import torch.nn as nn
from allennlp.nn.util import get_text_field_mask
import torch.nn.functional as F
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.matrix_attention.dot_product_matrix_attention import DotProductMatrixAttention


def __init__(self, conv_output_size: List[int], conv_kernel_size: List[Tuple[(int, int)]], adaptive_pooling_size: List[Tuple[(int, int)]]):
    super(MatchPyramid, self).__init__()
    self.cosine_module = CosineMatrixAttention()
    if ((len(conv_output_size) != len(conv_kernel_size)) or (len(conv_output_size) != len(adaptive_pooling_size))):
        raise Exception('conv_output_size, conv_kernel_size, adaptive_pooling_size must have the same length')
    conv_layer_dict = OrderedDict()
    last_channel_out = 1
    for i in range(len(conv_output_size)):
        conv_layer_dict[('pad ' + str(i))] = nn.ConstantPad2d((0, (conv_kernel_size[i][0] - 1), 0, (conv_kernel_size[i][1] - 1)), 0)
        conv_layer_dict[('conv ' + str(i))] = nn.Conv2d(kernel_size=conv_kernel_size[i], in_channels=last_channel_out, out_channels=conv_output_size[i])
        conv_layer_dict[('relu ' + str(i))] = nn.ReLU()
        conv_layer_dict[('pool ' + str(i))] = nn.AdaptiveMaxPool2d(adaptive_pooling_size[i])
        last_channel_out = conv_output_size[i]
    self.conv_layers = nn.Sequential(conv_layer_dict)
    self.dense = nn.Linear(((conv_output_size[(- 1)] * adaptive_pooling_size[(- 1)][0]) * adaptive_pooling_size[(- 1)][1]), out_features=100, bias=True)
    self.dense2 = nn.Linear(100, out_features=10, bias=True)
    self.dense3 = nn.Linear(10, out_features=1, bias=False)

import torch
from torch import nn
from torch.nn import functional as F
from models.utils import round_filters, round_repeats, drop_connect, get_same_padding_conv2d, get_model_params, efficientnet_params, load_pretrained_weights, Swish, MemoryEfficientSwish

if (__name__ == '__main__'):
    model = EfficientNet.from_pretrained('efficientnet-b0')
    inputs = torch.randn(4, 3, 640, 640)
    P = model(inputs)
    for (idx, p) in enumerate(P):
        print('P{}: {}'.format(idx, p.size()))

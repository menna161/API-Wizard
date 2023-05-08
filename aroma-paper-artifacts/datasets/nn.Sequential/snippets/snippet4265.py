import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from utils.utils import mIoULoss, to_one_hot


def get_encoder_block(n=2):
    seq = nn.Sequential()
    seq.add_module(('regular%d_1' % n), RegularBottleneck(128, padding=1, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('dilated%d_2' % n), RegularBottleneck(128, dilation=2, padding=2, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('asymmetric%d_3' % n), RegularBottleneck(128, kernel_size=5, padding=2, asymmetric=True, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('dilated%d_4' % n), RegularBottleneck(128, dilation=4, padding=4, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('regular%d_5' % n), RegularBottleneck(128, padding=1, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('dilated%d_6' % n), RegularBottleneck(128, dilation=8, padding=8, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('asymmetric%d_7' % n), RegularBottleneck(128, kernel_size=5, asymmetric=True, padding=2, dropout_prob=0.1, relu=encoder_relu))
    seq.add_module(('dilated%d_8' % n), RegularBottleneck(128, dilation=16, padding=16, dropout_prob=0.1, relu=encoder_relu))
    return seq

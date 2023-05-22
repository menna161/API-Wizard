import torch
import torch.nn as nn
import torch.nn.functional as F
from complex_layers.cmplx_conv import ComplexConv1d, ComplexConv2d, ComplexConv3d
from complex_layers.cmplx_activation import CReLU, ModReLU, ZReLU
from complex_layers.cmplx_upsample import ComplexUpsample
from complex_layers.radial_bn import RadialBatchNorm1d, RadialBatchNorm2d, RadialBatchNorm3d
from complex_layers.cmplx_dropout import ComplexDropout
from configs import config


def __init__(self, in_ch, out_ch, residual_connection=True):
    super(BottleNeck, self).__init__()
    self.residual_connection = residual_connection
    self.down_conv = DownConv(in_ch)
    self.double_conv = nn.Sequential(complex_conv(in_ch, (2 * in_ch), padding=1), batch_norm((2 * in_ch)), activation((2 * in_ch)), ComplexDropout(config.dropout_ratio), complex_conv((2 * in_ch), out_ch, padding=1), batch_norm(out_ch), activation(out_ch), ComplexDropout(config.dropout_ratio))

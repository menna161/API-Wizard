import torch.nn as nn
from octconv import *


def conv_dw(inp, oup, stride, alpha_in=0.5, alpha_out=0.5):
    return nn.Sequential(Conv_BN_ACT(inp, inp, kernel_size=3, stride=stride, padding=1, groups=inp, bias=False, alpha_in=alpha_in, alpha_out=(alpha_in if (alpha_out != alpha_in) else alpha_out)), Conv_BN_ACT(inp, oup, kernel_size=1, alpha_in=alpha_in, alpha_out=alpha_out))

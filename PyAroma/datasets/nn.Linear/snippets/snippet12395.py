import torch
from torch import nn
from torch.nn import DataParallel
from torch.nn.parallel import DistributedDataParallel
import torch.backends.cudnn as cudnn
import numpy as np
from FastAutoAugment.networks.resnet import ResNet
from FastAutoAugment.networks.pyramidnet import PyramidNet
from FastAutoAugment.networks.shakeshake.shake_resnet import ShakeResNet
from FastAutoAugment.networks.wideresnet import WideResNet
from FastAutoAugment.networks.shakeshake.shake_resnext import ShakeResNeXt
from FastAutoAugment.networks.efficientnet_pytorch import EfficientNet, RoutingFn
from FastAutoAugment.tf_port.tpu_bn import TpuBatchNormalization


def kernel_initializer(module):

    def get_fan_in_out(module):
        num_input_fmaps = module.weight.size(1)
        num_output_fmaps = module.weight.size(0)
        receptive_field_size = 1
        if (module.weight.dim() > 2):
            receptive_field_size = module.weight[0][0].numel()
        fan_in = (num_input_fmaps * receptive_field_size)
        fan_out = (num_output_fmaps * receptive_field_size)
        return (fan_in, fan_out)
    if isinstance(module, torch.nn.Conv2d):
        (fan_in, fan_out) = get_fan_in_out(module)
        torch.nn.init.normal_(module.weight, mean=0.0, std=np.sqrt((2.0 / fan_out)))
        if (module.bias is not None):
            torch.nn.init.constant_(module.bias, val=0.0)
    elif isinstance(module, RoutingFn):
        torch.nn.init.xavier_uniform_(module.weight)
        torch.nn.init.constant_(module.bias, val=0.0)
    elif isinstance(module, torch.nn.Linear):
        (fan_in, fan_out) = get_fan_in_out(module)
        delta = (1.0 / np.sqrt(fan_out))
        torch.nn.init.uniform_(module.weight, a=(- delta), b=delta)
        if (module.bias is not None):
            torch.nn.init.constant_(module.bias, val=0.0)

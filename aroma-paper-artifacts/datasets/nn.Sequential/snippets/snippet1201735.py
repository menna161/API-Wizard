from collections import OrderedDict
import math
import torch
import torch.nn as nn
from torch.utils import model_zoo
from torch.nn import BatchNorm2d


def __init__(self, block, layers, groups, reduction, dropout_p=0.2, inplanes=128, input_3x3=True, downsample_kernel_size=3, downsample_padding=1, num_classes=1000):
    '\n        Parameters\n        ----------\n        block (nn.Module): Bottleneck class.\n            - For SENet154: SEBottleneck\n            - For SE-ResNet models: SEResNetBottleneck\n            - For SE-ResNeXt models:  SEResNeXtBottleneck\n        layers (list of ints): Number of residual blocks for 4 layers of the\n            network (layer1...layer4).\n        groups (int): Number of groups for the 3x3 convolution in each\n            bottleneck block.\n            - For SENet154: 64\n            - For SE-ResNet models: 1\n            - For SE-ResNeXt models:  32\n        reduction (int): Reduction ratio for Squeeze-and-Excitation modules.\n            - For all models: 16\n        dropout_p (float or None): Drop probability for the Dropout layer.\n            If `None` the Dropout layer is not used.\n            - For SENet154: 0.2\n            - For SE-ResNet models: None\n            - For SE-ResNeXt models: None\n        inplanes (int):  Number of input channels for layer1.\n            - For SENet154: 128\n            - For SE-ResNet models: 64\n            - For SE-ResNeXt models: 64\n        input_3x3 (bool): If `True`, use three 3x3 convolutions instead of\n            a single 7x7 convolution in layer0.\n            - For SENet154: True\n            - For SE-ResNet models: False\n            - For SE-ResNeXt models: False\n        downsample_kernel_size (int): Kernel size for downsampling convolutions\n            in layer2, layer3 and layer4.\n            - For SENet154: 3\n            - For SE-ResNet models: 1\n            - For SE-ResNeXt models: 1\n        downsample_padding (int): Padding for downsampling convolutions in\n            layer2, layer3 and layer4.\n            - For SENet154: 1\n            - For SE-ResNet models: 0\n            - For SE-ResNeXt models: 0\n        num_classes (int): Number of outputs in `last_linear` layer.\n            - For all models: 1000\n        '
    super(SENet, self).__init__()
    self.inplanes = inplanes
    if input_3x3:
        layer0_modules = [('conv1', nn.Conv2d(4, 64, 3, stride=2, padding=1, bias=False)), ('bn1', BatchNorm2d(64)), ('relu1', nn.ReLU(inplace=True)), ('conv2', nn.Conv2d(64, 64, 3, stride=1, padding=1, bias=False)), ('bn2', BatchNorm2d(64)), ('relu2', nn.ReLU(inplace=True)), ('conv3', nn.Conv2d(64, inplanes, 3, stride=1, padding=1, bias=False)), ('bn3', BatchNorm2d(inplanes)), ('relu3', nn.ReLU(inplace=True))]
    else:
        layer0_modules = [('conv1', nn.Conv2d(4, inplanes, kernel_size=7, stride=2, padding=3, bias=False)), ('bn1', BatchNorm2d(inplanes)), ('relu1', nn.ReLU(inplace=True))]
    self.pool = nn.MaxPool2d(3, stride=2, ceil_mode=True)
    self.layer0 = nn.Sequential(OrderedDict(layer0_modules))
    self.layer1 = self._make_layer(block, planes=64, blocks=layers[0], groups=groups, reduction=reduction, downsample_kernel_size=1, downsample_padding=0)
    self.layer2 = self._make_layer(block, planes=128, blocks=layers[1], stride=2, groups=groups, reduction=reduction, downsample_kernel_size=downsample_kernel_size, downsample_padding=downsample_padding)
    self.layer3 = self._make_layer(block, planes=256, blocks=layers[2], stride=2, groups=groups, reduction=reduction, downsample_kernel_size=downsample_kernel_size, downsample_padding=downsample_padding)
    self.layer4 = self._make_layer(block, planes=512, blocks=layers[3], stride=2, groups=groups, reduction=reduction, downsample_kernel_size=downsample_kernel_size, downsample_padding=downsample_padding)
    self.avg_pool = nn.AvgPool2d(7, stride=1)
    self.dropout = (nn.Dropout(dropout_p) if (dropout_p is not None) else None)
    self.last_linear = nn.Linear((512 * block.expansion), num_classes)
    self._initialize_weights()

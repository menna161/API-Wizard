import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import sys
import Utils


def __init__(self, block, layers, num_classes=1000, zero_init_residual=False, padding='ZeroPad'):
    super(ResNet, self).__init__()
    self.padding = getattr(Utils.CubePad, padding)
    self.inplanes = 64
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=0, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
    self.layer1 = self._make_layer(block, 64, layers[0], padding=self.padding)
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2, padding=self.padding)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2, padding=self.padding)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2, padding=self.padding)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear((512 * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
    if zero_init_residual:
        for m in self.modules():
            if isinstance(m, Bottleneck):
                nn.init.constant_(m.bn3.weight, 0)
            elif isinstance(m, BasicBlock):
                nn.init.constant_(m.bn2.weight, 0)

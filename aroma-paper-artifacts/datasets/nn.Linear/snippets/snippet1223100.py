from torch import nn
from torchvision.models.utils import load_state_dict_from_url
from networks import layers
from networks.blocks import InvertedResidual, ConvBNNonLinear


def __init__(self, nc, num_classes=1000, width_mult=1.0, inverted_residual_setting=None, round_nearest=8):
    '\n        The init function of the  MobileNet V2 Module\n\n        :param nc: Network controller\n        :param num_classes: the number of output classes\n        :param width_mult: The width multiple\n        :param inverted_residual_setting: A list of the block configurations\n        :param round_nearest: Rounding to nearest value\n        '
    super(MobileNetV2, self).__init__()
    block = InvertedResidual
    input_channel = 32
    last_channel = 1280
    if (inverted_residual_setting is None):
        inverted_residual_setting = [[1, 16, 1, 1], [6, 24, 2, 2], [6, 32, 3, 2], [6, 64, 4, 2], [6, 96, 3, 1], [6, 160, 3, 2], [6, 320, 1, 1]]
    if ((len(inverted_residual_setting) == 0) or (len(inverted_residual_setting[0]) != 4)):
        raise ValueError('inverted_residual_setting should be non-empty or a 4-element list, got {}'.format(inverted_residual_setting))
    input_channel = _make_divisible((input_channel * width_mult), round_nearest)
    self.last_channel = _make_divisible((last_channel * max(1.0, width_mult)), round_nearest)
    features = [ConvBNNonLinear(nc, 3, input_channel, stride=2)]
    for (t, c, n, s) in inverted_residual_setting:
        output_channel = _make_divisible((c * width_mult), round_nearest)
        for i in range(n):
            stride = (s if (i == 0) else 1)
            features.append(block(nc, input_channel, output_channel, stride, expand_ratio=t))
            input_channel = output_channel
    features.append(ConvBNNonLinear(nc, input_channel, self.last_channel, kernel_size=1))
    self.features = nn.Sequential(*features)
    self.classifier = nn.Sequential(nn.Dropout(0.2), layers.FullyConnected(nc, self.last_channel, num_classes))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')
            if (m.bias is not None):
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.ones_(m.weight)
            nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.01)
            nn.init.zeros_(m.bias)

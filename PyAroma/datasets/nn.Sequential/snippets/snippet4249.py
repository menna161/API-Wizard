import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


def net_init(self, input_size, ms_ks):
    (input_w, input_h) = input_size
    self.fc_input_feature = ((5 * int((input_w / 16))) * int((input_h / 16)))
    self.backbone = models.vgg16_bn(pretrained=self.pretrained).features
    for i in [34, 37, 40]:
        conv = self.backbone._modules[str(i)]
        dilated_conv = nn.Conv2d(conv.in_channels, conv.out_channels, conv.kernel_size, stride=conv.stride, padding=tuple(((p * 2) for p in conv.padding)), dilation=2, bias=(conv.bias is not None))
        dilated_conv.load_state_dict(conv.state_dict())
        self.backbone._modules[str(i)] = dilated_conv
    self.backbone._modules.pop('33')
    self.backbone._modules.pop('43')
    self.layer1 = nn.Sequential(nn.Conv2d(512, 1024, 3, padding=4, dilation=4, bias=False), nn.BatchNorm2d(1024), nn.ReLU(), nn.Conv2d(1024, 128, 1, bias=False), nn.BatchNorm2d(128), nn.ReLU())
    self.message_passing = nn.ModuleList()
    self.message_passing.add_module('up_down', nn.Conv2d(128, 128, (1, ms_ks), padding=(0, (ms_ks // 2)), bias=False))
    self.message_passing.add_module('down_up', nn.Conv2d(128, 128, (1, ms_ks), padding=(0, (ms_ks // 2)), bias=False))
    self.message_passing.add_module('left_right', nn.Conv2d(128, 128, (ms_ks, 1), padding=((ms_ks // 2), 0), bias=False))
    self.message_passing.add_module('right_left', nn.Conv2d(128, 128, (ms_ks, 1), padding=((ms_ks // 2), 0), bias=False))
    self.layer2 = nn.Sequential(nn.Dropout2d(0.1), nn.Conv2d(128, 5, 1))
    self.layer3 = nn.Sequential(nn.Softmax(dim=1), nn.AvgPool2d(2, 2))
    self.fc = nn.Sequential(nn.Linear(self.fc_input_feature, 128), nn.ReLU(), nn.Linear(128, 4), nn.Sigmoid())

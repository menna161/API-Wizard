import torch.nn as nn
import torch
from ltr.models.layers.blocks import LinearBlock
from ltr.external.PreciseRoIPooling.pytorch.prroi_pool import PrRoIPool2D


def __init__(self, input_dim=(128, 256), pred_input_dim=(256, 256), pred_inter_dim=(256, 256)):
    super().__init__()
    self.conv3_1r = conv(input_dim[0], 128, kernel_size=3, stride=1)
    self.conv3_1t = conv(input_dim[0], 256, kernel_size=3, stride=1)
    self.conv3_2t = conv(256, pred_input_dim[0], kernel_size=3, stride=1)
    self.prroi_pool3r = PrRoIPool2D(3, 3, (1 / 8))
    self.prroi_pool3t = PrRoIPool2D(5, 5, (1 / 8))
    self.fc3_1r = conv(128, 256, kernel_size=3, stride=1, padding=0)
    self.conv4_1r = conv(input_dim[1], 256, kernel_size=3, stride=1)
    self.conv4_1t = conv(input_dim[1], 256, kernel_size=3, stride=1)
    self.conv4_2t = conv(256, pred_input_dim[1], kernel_size=3, stride=1)
    self.prroi_pool4r = PrRoIPool2D(1, 1, (1 / 16))
    self.prroi_pool4t = PrRoIPool2D(3, 3, (1 / 16))
    self.fc34_3r = conv((256 + 256), pred_input_dim[0], kernel_size=1, stride=1, padding=0)
    self.fc34_4r = conv((256 + 256), pred_input_dim[1], kernel_size=1, stride=1, padding=0)
    self.fc3_rt = LinearBlock(pred_input_dim[0], pred_inter_dim[0], 5)
    self.fc4_rt = LinearBlock(pred_input_dim[1], pred_inter_dim[1], 3)
    self.iou_predictor = nn.Linear((pred_inter_dim[0] + pred_inter_dim[1]), 1, bias=True)
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d) or isinstance(m, nn.Linear)):
            nn.init.kaiming_normal_(m.weight.data, mode='fan_in')
            if (m.bias is not None):
                m.bias.data.zero_()

import torch
from torch import nn
import torch.nn.functional as F
from .senet import se_resnext50_32x4d, senet154, se_resnext101_32x4d
from .dpn import dpn92


def __init__(self, pretrained='imagenet+5k', **kwargs):
    super(Dpn92_9ch_Unet, self).__init__()
    encoder_filters = [64, 336, 704, 1552, 2688]
    decoder_filters = [64, 96, 128, 256, 512]
    self.conv6 = ConvRelu(encoder_filters[(- 1)], decoder_filters[(- 1)])
    self.conv6_2 = nn.Sequential(ConvRelu(((((decoder_filters[(- 1)] + encoder_filters[(- 2)]) + 2) + 27) + 2), decoder_filters[(- 1)]), SCSEModule(decoder_filters[(- 1)], reduction=16, concat=True))
    self.conv7 = ConvRelu((decoder_filters[(- 1)] * 2), decoder_filters[(- 2)])
    self.conv7_2 = nn.Sequential(ConvRelu(((((decoder_filters[(- 2)] + encoder_filters[(- 3)]) + 2) + 27) + 2), decoder_filters[(- 2)]), SCSEModule(decoder_filters[(- 2)], reduction=16, concat=True))
    self.conv8 = ConvRelu((decoder_filters[(- 2)] * 2), decoder_filters[(- 3)])
    self.conv8_2 = nn.Sequential(ConvRelu(((((decoder_filters[(- 3)] + encoder_filters[(- 4)]) + 2) + 27) + 2), decoder_filters[(- 3)]), SCSEModule(decoder_filters[(- 3)], reduction=16, concat=True))
    self.conv9 = ConvRelu((decoder_filters[(- 3)] * 2), decoder_filters[(- 4)])
    self.conv9_2 = nn.Sequential(ConvRelu(((((decoder_filters[(- 4)] + encoder_filters[(- 5)]) + 2) + 27) + 2), decoder_filters[(- 4)]), SCSEModule(decoder_filters[(- 4)], reduction=16, concat=True))
    self.conv10 = ConvRelu(((((decoder_filters[(- 4)] * 2) + 2) + 2) + 27), decoder_filters[(- 5)])
    self.res = nn.Conv2d(((decoder_filters[(- 5)] + 2) + 2), 4, 1, stride=1, padding=0)
    self.off_nadir = nn.Sequential(nn.Linear(encoder_filters[(- 1)], 64), nn.ReLU(inplace=True), nn.Linear(64, 1))
    self._initialize_weights()
    encoder = dpn92(pretrained=pretrained)
    conv1_new = nn.Conv2d(9, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    _w = encoder.blocks['conv1_1'].conv.state_dict()
    _w['weight'] = torch.cat([(0.8 * _w['weight']), (0.1 * _w['weight']), (0.1 * _w['weight'])], 1)
    conv1_new.load_state_dict(_w)
    self.conv1 = nn.Sequential(conv1_new, encoder.blocks['conv1_1'].bn, encoder.blocks['conv1_1'].act)
    self.conv2 = nn.Sequential(encoder.blocks['conv1_1'].pool, *[b for (k, b) in encoder.blocks.items() if k.startswith('conv2_')])
    self.conv3 = nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv3_')])
    self.conv4 = nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv4_')])
    self.conv5 = nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv5_')])

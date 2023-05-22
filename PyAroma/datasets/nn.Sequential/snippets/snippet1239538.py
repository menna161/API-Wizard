import torch
from torch import nn
import torchvision


def __init__(self, encoded_image_size=14):
    super(Encoder, self).__init__()
    self.enc_image_size = encoded_image_size
    resnet = torchvision.models.resnet101(pretrained=True)
    modules = list(resnet.children())[:(- 2)]
    self.resnet = nn.Sequential(*modules)
    self.adaptive_pool = nn.AdaptiveAvgPool2d((encoded_image_size, encoded_image_size))
    self.fine_tune()

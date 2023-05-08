import torch
import torch.nn as nn
import torchvision


def __init__(self, requires_grad=False):
    super(PerceptualLoss, self).__init__()
    mean_rgb = torch.FloatTensor([0.485, 0.456, 0.406])
    std_rgb = torch.FloatTensor([0.229, 0.224, 0.225])
    self.register_buffer('mean_rgb', mean_rgb)
    self.register_buffer('std_rgb', std_rgb)
    vgg_pretrained_features = torchvision.models.vgg16(pretrained=True).features
    self.slice1 = nn.Sequential()
    self.slice2 = nn.Sequential()
    self.slice3 = nn.Sequential()
    self.slice4 = nn.Sequential()
    for x in range(4):
        self.slice1.add_module(str(x), vgg_pretrained_features[x])
    for x in range(4, 9):
        self.slice2.add_module(str(x), vgg_pretrained_features[x])
    for x in range(9, 16):
        self.slice3.add_module(str(x), vgg_pretrained_features[x])
    for x in range(16, 23):
        self.slice4.add_module(str(x), vgg_pretrained_features[x])
    if (not requires_grad):
        for param in self.parameters():
            param.requires_grad = False

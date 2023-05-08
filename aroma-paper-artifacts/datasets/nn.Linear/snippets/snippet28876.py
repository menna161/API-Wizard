import torch, os, numpy as np
import torch.nn as nn
import pretrainedmodels as ptm
import pretrainedmodels.utils as utils
import torchvision.models as models
import googlenet


def __init__(self, opt, list_style=False, no_norm=False):
    super(ResNet50, self).__init__()
    self.pars = opt
    if (not opt.not_pretrained):
        print('Getting pretrained weights...')
        self.model = ptm.__dict__['resnet50'](num_classes=1000, pretrained='imagenet')
        print('Done.')
    else:
        print('Not utilizing pretrained weights!')
        self.model = ptm.__dict__['resnet50'](num_classes=1000, pretrained=None)
    for module in filter((lambda m: (type(m) == nn.BatchNorm2d)), self.model.modules()):
        module.eval()
        module.train = (lambda _: None)
    self.model.last_linear = torch.nn.Linear(self.model.last_linear.in_features, opt.embed_dim)
    self.layer_blocks = nn.ModuleList([self.model.layer1, self.model.layer2, self.model.layer3, self.model.layer4])

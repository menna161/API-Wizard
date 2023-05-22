import torch, os, numpy as np
import torch.nn as nn
import pretrainedmodels as ptm
import pretrainedmodels.utils as utils
import torchvision.models as models
import googlenet


def __init__(self, opt):
    '\n        Args:\n            opt: argparse.Namespace, contains all training-specific parameters.\n        Returns:\n            Nothing!\n        '
    super(GoogLeNet, self).__init__()
    self.pars = opt
    self.model = googlenet.googlenet(num_classes=1000, pretrained=('imagenet' if (not opt.not_pretrained) else False))
    for module in filter((lambda m: (type(m) == nn.BatchNorm2d)), self.model.modules()):
        module.eval()
        module.train = (lambda _: None)
    rename_attr(self.model, 'fc', 'last_linear')
    self.layer_blocks = nn.ModuleList([self.model.inception3a, self.model.inception3b, self.model.maxpool3, self.model.inception4a, self.model.inception4b, self.model.inception4c, self.model.inception4d, self.model.inception4e, self.model.maxpool4, self.model.inception5a, self.model.inception5b, self.model.avgpool])
    self.model.last_linear = torch.nn.Linear(self.model.last_linear.in_features, opt.embed_dim)

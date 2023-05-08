import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F


def __init__(self, network, fixconvs=False, nopretrained=True):
    super(ResNet18, self).__init__()
    self.model = network(pretrained=nopretrained)
    if fixconvs:
        for param in self.model.parameters():
            param.requires_grad = False
    self.regressor = nn.Linear(self.model.fc.in_features, 300)
    self.dropout = torch.nn.Dropout(p=0.05)
    self.model = torch.nn.Sequential(*list(self.model.children())[:(- 1)])

import torch
from torch import nn
import numpy as np
from .VisualSemanticModel import VisualSemanticModel
import torchvision.models as models
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


def __init__(self, embed_size, finetune=True):
    super(BaseImageEncoder, self).__init__()
    self.embed_size = embed_size
    self.cnn = models.resnet18(pretrained=True).to(device)
    for param in self.cnn.parameters():
        param.requires_grad = finetune
    self.fc = nn.Linear(self.cnn.fc.in_features, embed_size).to(device)
    self.cnn.fc = nn.Sequential()
    self.init_weights()

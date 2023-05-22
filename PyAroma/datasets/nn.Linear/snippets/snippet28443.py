import torch.nn as nn
from utils import *


def __init__(self, num_classes=1000, feat_dim=2048, *args):
    super(DotProduct_Classifier, self).__init__()
    self.fc = nn.Linear(feat_dim, num_classes)

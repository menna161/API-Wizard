import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_fconv_lpf import *


def __init__(self, features, num_classes=1000, init_weights=True):
    super(VGG, self).__init__()
    self.features = features
    self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
    self.classifier = nn.Sequential(nn.Linear(((512 * 7) * 7), 4096), nn.ReLU(True), nn.Dropout(), nn.Linear(4096, 4096), nn.ReLU(True), nn.Dropout(), nn.Linear(4096, num_classes))
    if init_weights:
        self._initialize_weights()

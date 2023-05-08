import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, numClasses, aux=False, **kwargs):
    super(FastSCNN, self).__init__()
    self.aux = aux
    self.learningToDownSample = LearningToDownSample(32, 48, 64)
    self.globalFeatureExtractor = GlobalFeatureExtractor(64, [64, 96, 128], 128, 6, [3, 3, 3])
    self.featureFusion = FeatureFusion(64, 128, 128)
    self.classifier = Classifier(128, numClasses)
    if (self.aux is not None):
        self.auxlayer = nn.Sequential(nn.Conv2d(64, 32, 3, padding=1, bias=False), nn.BatchNorm2d(32), nn.ReLU(True), nn.Dropout(0.1), nn.Conv2d(32, numClasses, 1))

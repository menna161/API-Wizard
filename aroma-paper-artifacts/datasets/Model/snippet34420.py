import torch.nn as nn
from torch.nn import init
import resnet


def forward(self, x):
    (x3, x4) = self.Backbone(x)
    classification = self.classificationModel(x3)
    regression = self.regressionModel(x4)
    if self.is_3D:
        DepthRegressionModel = self.DepthRegressionModel(x4)
        return (classification, regression, DepthRegressionModel)
    return (classification, regression)
